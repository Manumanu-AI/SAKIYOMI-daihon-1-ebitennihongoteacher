import requests
import json
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pinecone
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import langchain
from openai import OpenAI
import streamlit as st
from example_plot import example_plot
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.callbacks import tracing_v2_enabled

apify_wcc_endpoint = st.secrets['website_content_crawler_endpoint']
apifyapi_key = st.secrets['apifyapi_key']
pinecone_api_key = st.secrets['PINECONE_API_KEY']
pinecone_index_name = st.secrets['PINECONE_INDEX_NAME']
openai_api_key = st.secrets['OPENAI_API_KEY']


# URLからコンテンツをスクレイピングする関数
def scrape_url(url):
    try:
        print(f"scrape_url: URL = {url}")  # デバッグ用プリント
        headers = {"Authorization": f"Bearer {apifyapi_key}"}
        payload = {"startUrls": [{"url": url}]}
        response = requests.post(apify_wcc_endpoint, json=payload, headers=headers)

        # print(f"scrape_url: Response = {response.text[:100]}...")  # デバッグ用プリント（応答の最初の100文字を表示）
        if response.status_code in [200, 201]:
            return response.text
        else:
            raise Exception(f"ステータスコード: {response.status_code}, レスポンス: {response.text}")
    except Exception as e:
        raise Exception(f"scrape_urlでエラーが発生しました: {e}")


    
# データ内の必要なキーだけを取得する関数
def extract_keys_from_json(json_data):
    data = json.loads(json_data)
    extracted_data = []
    for item in data:
        formatted_data = {
            'url': item.get('url', ''),
            'description': item.get('metadata', {}).get('description', ''),
            'title': item.get('metadata', {}).get('title', ''),
            'text': item.get('text', ''),
            'keywords': item.get('metadata', {}).get('keywords', '')
        }
        extracted_data.append(formatted_data)
    return extracted_data


# テキストとメタデータを準備
def prepare_text_and_metadata(combined_data):
    texts = []
    metadata_list = []

    for item in combined_data:
        # テキスト部分の抽出と結合
        texts.append(item['text'])

        # メタデータの抽出
        metadata = {
            "original_url": item.get('url', ''),
            "description": item.get('description', '') if item.get('description') is not None else '',
            "title": item.get('title', '') if item.get('title') is not None else '',
            "keywords": item.get('keywords', '')  # Noneの場合は空文字列を返す
        }
        if metadata["keywords"]:  # キーワードが存在する場合のみ分割
            metadata["keywords"] = metadata["keywords"].split(', ')
        else:
            metadata["keywords"] = []  # キーワードがNoneまたは空の場合、空のリストを割り当てる

        metadata_list.append(metadata)

    # すべてのテキストを一つの文字列に結合
    combined_text = " ".join(texts)

    return combined_text, metadata_list




# テキストをチャンクに
def split_text(combined_text):
    set_chunk_length = 1000
    set_chunk_overlap = 100
    chunks = RecursiveCharacterTextSplitter(chunk_size = set_chunk_length, chunk_overlap = set_chunk_overlap)
    return chunks.split_text(combined_text)

from sentence_transformers import SentenceTransformer

def make_chunks_embeddings(chunks):
    # モデルのロード
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 
    embeddings = model.encode(chunks)

    return embeddings



### pinecone処理
def initialize_pinecone():
    pinecone = Pinecone(api_key=pinecone_api_key)
    index = pinecone.Index(pinecone_index_name)
    return index


def store_data_in_pinecone(index, chunk_embeddings, chunks, metadata_list, namespace):
    # 最初のメタデータを使用（共通部分）
    common_metadata = metadata_list[0]

    vectors_to_upsert = []
    for i, (embedding, chunk) in enumerate(zip(chunk_embeddings, chunks)):
        # 一意のIDの生成
        unique_id = f"{common_metadata['original_url']}-chunk-{i}"

        # メタデータにテキストチャンクを追加
        metadata = {
            "original_url": common_metadata['original_url'],
            "description": common_metadata['description'],
            "title": common_metadata['title'],
            "keywords": common_metadata['keywords'],
            "text_chunk": chunk  # テキストチャンクを追加
        }

        # ベクトルとメタデータをリストに追加
        vectors_to_upsert.append({
            "id": unique_id,
            "values": embedding.tolist(),  # numpy配列をリストに変換
            "metadata": metadata
        })

    # 一度に全てのベクトルをアップロード
    index.upsert(vectors=vectors_to_upsert, namespace=namespace)

    # 保存したIDをプリント（オプション）
    for vector in vectors_to_upsert:
        print(f"Saved: {vector['id']}")



# クエリの埋め込みベクトルを生成する関数
def generate_query_embedding(query):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode([query])[0]

# シミラリティ検索を実行する関数
def perform_similarity_search(index, query, namespace, top_k=3):
    query_embedding = generate_query_embedding(query)
    return index.query(
        namespace=namespace,
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )
    
def delete_all_data_in_namespace(index, namespace):
    index.delete(delete_all=True, namespace=namespace)
    print(f"次のネームスペースから全データが削除されました： '{namespace}'.")



def delete_data_by_url(index, namespace, url):
    # 名前空間内のすべてのIDを取得
    all_ids = index.describe_index_stats(namespace=namespace)["namespaces"][namespace]["ids"]
    
    # 指定されたURLに基づいてIDをフィルタリング
    ids_to_delete = [id for id in all_ids if url in id]
    
    # フィルタリングされたIDを削除
    index.delete(ids=ids_to_delete, namespace=namespace)
    print(f"ネームスペース【'{namespace}'】から次のURLの全データ削除されました【'{url}'】.")


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def store_pdf_data_in_pinecone(index, chunk_embeddings, chunks, pdf_file_name, namespace):
    vectors_to_upsert = []
    for i, (embedding, chunk) in enumerate(zip(chunk_embeddings, chunks)):
        unique_id = f"pdf-chunk-{i}"  # PDFチャンクのIDを設定
        # メタデータにファイル名を使用
        metadata = {
            "pdf_filename": pdf_file_name,  # ファイル名をoriginal_urlとして使用
            "title": pdf_file_name,  # ファイル名をタイトルとして使用
            "description": "",  # 説明は空
            "keywords": [],  # キーワードは空のリスト
            "text_chunk": chunk  # テキストチャンクを追加
        }
        # ベクトルとメタデータをリストに追加
        vectors_to_upsert.append({
            "id": unique_id,
            "values": embedding.tolist(),
            "metadata": metadata
        })
    # 一度に全てのベクトルをアップロード
    index.upsert(vectors=vectors_to_upsert, namespace=namespace)
    # 保存したIDをプリント（オプション）
    for vector in vectors_to_upsert:
        print(f"Saved: {vector['id']}")



def generate_response_with_llm_for_multiple_namespaces(index, user_input, namespaces):
    results = {}  # 各名前空間の検索結果を格納する辞書

    # 名前空間ごとに検索結果を取得
    for ns in namespaces:
        try:
            query_embedding = generate_query_embedding(user_input)
            search_results = index.query(
                namespace=ns,
                vector=query_embedding.tolist(),
                top_k=3,
                include_metadata=True
            )
            if ns == "ns3":
                # ns3のメタデータを直接利用する特別な処理
                if search_results['matches']:
                    metadata = search_results['matches'][0]['metadata']
                    # 新しいメタデータ形式に基づいて内容を整形してLLMに渡す
                    results[ns] = "\n".join([f"{key}: {value}" for key, value in metadata.items()])
            else:
                # 他の名前空間の処理は変更なし
                result_texts = [result['metadata']['text_chunk'] for result in search_results['matches']]
                results[ns] = " ".join(result_texts) if result_texts else "情報なし"
        except KeyError as e:
            print(f"エラーが発生しました: 名前空間 '{ns}' で {e} キーが見つかりません。")
            results[ns] = "エラー: 検索結果が見つかりませんでした。"

    # プロンプトテンプレートの準備
    prompt_template = PromptTemplate.from_template("""
    输出应以中文为主要语言。
    あなたはInstagramフィードの台本専門の作家です。
    中国人向けに、日本語フレーズを学ぶ投稿を作ってもらいます。
    ユーザーメッセージに従い、中国語でInstagramのフィード台本を生成してください。
    ユーザーは日本語でインプットをしますが、あなたがアウトプットする台本の言語は中国語です。そのためタイトルから中国語でお願いします。
    台本は中国語で書いて、フレーズを紹介するときだけ日本語と中国語をセットで使ってください。
    ----------
    【ユーザーのメッセージ】
    {user_input}
    
    ----------
    【台本作成時のポイント】
    ・必ずビジネス・仕事の場で使える日本語についての台本を書くこと。
    ・フレーズを紹介するときは、日本語、中国語、台湾語の3つセットで作ること。
    ・ユーザーインプットの「テーマ」を安直にタイトルに持ってくるのではなく、【過去Instagramで投稿された台本】の"1枚目-表紙 (タイトル)"キーを参照して、適切なタイトルをつけなさい。その際、テーマを自分なりに細分化し、超限定的なテーマを一つ主観で選び投稿を作って下さい。そうすることで、ユーザーは同じ指示で様々なバリエーションを得られます。
    ・合計8枚以上、10枚以下で書いてください。
    ・1枚目(表紙)は「フック」と「ベース」で構成されています。「フック」と「ベース」の文字数の合計が24文字以内になるようにしてください。
    ・練習問題を出すときは、必ず次のページに回答と解説を掲載してください。

    ----------
    その際、「過去Instagramで投稿された台本」の情報と口調を参照すること。
    また、今回ユーザーが希望する【テーマの関連情報」を使ってください。
    ----------
    【テーマの関連情報】
    {results_ns1}
    {results_ns2}
    ----------
    【過去Instagramで投稿された台本】
    {results_ns3}
    ----------
    生成する台本のフォーマットは【アウトプット例】と同じにして生成してください。
    ----------
    【アウトプット例】
    {example_plot}
    """)

    # LLMにプロンプトを渡して応答を生成
    llm = ChatOpenAI(model='gpt-4-1106-preview', temperature=0.7)
    llm_chain = LLMChain(prompt=prompt_template, llm=llm)

    # st.secretsを使ってプロジェクト名を取得
    project_name = st.secrets["LANGCHAIN_PROJECT"]

    with tracing_v2_enabled(project_name=project_name):
        response = llm_chain.invoke({
            "user_input": user_input,
            "results_ns1": results.get('ns1', '情報なし'),
            "results_ns2": results.get('ns2', '情報なし'),
            "results_ns3": results.get('ns3', '情報なし'),
            "example_plot": example_plot
        })
        return response
