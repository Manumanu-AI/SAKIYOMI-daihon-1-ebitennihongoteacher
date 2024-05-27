import streamlit as st
import streamlit.components.v1 as components
import re

# ページの設定
st.set_page_config(
    page_title="Canvaテンプレート",
    page_icon='🤖',
    layout='wide',
)

st.title('Canvaテンプレート')


st.sidebar.title('メニュー')

# タブの作成
tab1, tab2 = st.tabs(["投稿テンプレート", "CTAテンプレート(準備中)"])




with tab1:
    st.write('投稿作成が楽になるデザインテンプレートです。<br>カラーやフォントをカスタマイズしてご使用ください！', unsafe_allow_html=True)
    with st.expander('▶ この機能の使い方動画', expanded=False):
        st.markdown(
            """
            <iframe width="640" height="360" src="https://www.youtube.com/embed/SZjbQvWrXYA?si=qtcq6RAAH0kFY0Jf frameborder="0" allowfullscreen></iframe>
            """, unsafe_allow_html=True
        )

    # CanvaのURLのリストとボタンのリンク
    canva_items = [
        {
            "embed_url": "https://www.canva.com/design/DAGFLSPbwsQ/JCvjuwoBa9gW5eYfokggWg/view",
            "button_url": "https://www.canva.com/design/DAFf5KnMSsI/0jYScCGQ_Pj83v2RAm_36w/view?utm_content=DAFf5KnMSsI&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLSQm_oU/mbsnhOo2z5XW6Krr1I3PGg/view",
            "button_url": "https://www.canva.com/design/DAFO1ftprAA/Zpj4rNVqB4gy8UZ2SgvgMQ/view?utm_content=DAFO1ftprAA&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLcSuR_o/cbbDm_ymB3mFB7eTXpvXZA/view",
            "button_url": "https://www.canva.com/design/DAFf5KnMSsI/0jYScCGQ_Pj83v2RAm_36w/view?utm_content=DAFf5KnMSsI&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLR9H73s/HrPfu9sJdDxIlD0-vTXdbg/view",
            "button_url": "https://www.canva.com/design/DAFDxk5uaf0/B82mafUpqiKlYvPG2pC3eg/view?utm_content=DAFDxk5uaf0&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLQzcfOI/5kxozzhURKAoCEag4I4m8A/view",
            "button_url": "https://www.canva.com/design/DAFQmbG2Z_s/ZHkevvfxb-qGAWBq7dpWhw/view?utm_content=DAFQmbG2Z_s&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLUYw144/zdrcK7Wl2ldP_nJ-KEOMwQ/view",
            "button_url": "https://www.canva.com/design/DAFQmAjpl6M/7sOsbIPjmQ4-aPlHw5nZbQ/view?utm_content=DAFQmAjpl6M&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLTf9-tg/ZiZEnnWiqacBwIXy_EQe0g/view",
            "button_url": "https://www.canva.com/design/DAFDxRJf4gc/qZKcaRU2gBuuVH0m0r8TyA/view?utm_content=DAFDxRJf4gc&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        }
    ]

    # 3列に分けて表示
    col1, col2, col3 = st.columns(3)

    # Canvaの埋め込みコードとボタンを生成して表示
    for i, item in enumerate(canva_items):
        canva_embed_code = f'''
        <div style="position: relative; width: 100%; height: 0; padding-top: 125.0000%; padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0; margin: 0;" src="{item['embed_url']}?embed" allowfullscreen="allowfullscreen" allow="fullscreen"></iframe>
        </div>
        '''
        
        button_code = f'''
        <div style="text-align: center; margin-top: 10px;">
          <a href="{item['button_url']}" target="_blank" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">テンプレを使用する</a>
        </div>
        '''
        
        if i % 3 == 0:
            with col1:
                components.html(canva_embed_code + button_code, height=500)
        elif i % 3 == 1:
            with col2:
                components.html(canva_embed_code + button_code, height=500)
        else:
            with col3:
                components.html(canva_embed_code + button_code, height=500)



with tab2:
    st.write('「CTA」と呼ばれる投稿最終ページのテンプレートです。<br>まだ作成していない方はぜひこちらのテンプレから！', unsafe_allow_html=True)
    with st.expander('▶ この機能の使い方動画', expanded=False):
        st.markdown(
            """
            <iframe width="640" height="360" src="https://www.youtube.com/embed/SZjbQvWrXYA?si=qtcq6RAAH0kFY0Jf" frameborder="0" allowfullscreen></iframe>
            """, unsafe_allow_html=True
        )

    # CanvaのURLのリストとボタンのリンク
    canva_items = [
        {
            "embed_url": "https://www.canva.com/design/DAGFLSPbwsQ/JCvjuwoBa9gW5eYfokggWg/view",
            "button_url": "https://www.canva.com/design/DAFf5KnMSsI/0jYScCGQ_Pj83v2RAm_36w/view?utm_content=DAFf5KnMSsI&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLSQm_oU/mbsnhOo2z5XW6Krr1I3PGg/view",
            "button_url": "https://www.canva.com/design/DAFO1ftprAA/Zpj4rNVqB4gy8UZ2SgvgMQ/view?utm_content=DAFO1ftprAA&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLcSuR_o/cbbDm_ymB3mFB7eTXpvXZA/view",
            "button_url": "https://www.canva.com/design/DAFf5KnMSsI/0jYScCGQ_Pj83v2RAm_36w/view?utm_content=DAFf5KnMSsI&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLR9H73s/HrPfu9sJdDxIlD0-vTXdbg/view",
            "button_url": "https://www.canva.com/design/DAFDxk5uaf0/B82mafUpqiKlYvPG2pC3eg/view?utm_content=DAFDxk5uaf0&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLQzcfOI/5kxozzhURKAoCEag4I4m8A/view",
            "button_url": "https://www.canva.com/design/DAFQmbG2Z_s/ZHkevvfxb-qGAWBq7dpWhw/view?utm_content=DAFQmbG2Z_s&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLUYw144/zdrcK7Wl2ldP_nJ-KEOMwQ/view",
            "button_url": "https://www.canva.com/design/DAFQmAjpl6M/7sOsbIPjmQ4-aPlHw5nZbQ/view?utm_content=DAFQmAjpl6M&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLTf9-tg/ZiZEnnWiqacBwIXy_EQe0g/view",
            "button_url": "https://www.canva.com/design/DAFDxRJf4gc/qZKcaRU2gBuuVH0m0r8TyA/view?utm_content=DAFDxRJf4gc&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        }
    ]

    # 3列に分けて表示
    col1, col2, col3 = st.columns(3)

    # Canvaの埋め込みコードとボタンを生成して表示
    for i, item in enumerate(canva_items):
        canva_embed_code = f'''
        <div style="position: relative; width: 100%; height: 0; padding-top: 125.0000%; padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0; margin: 0;" src="{item['embed_url']}?embed" allowfullscreen="allowfullscreen" allow="fullscreen"></iframe>
        </div>
        '''
        
        button_code = f'''
        <div style="text-align: center; margin-top: 10px;">
          <a href="{item['button_url']}" target="_blank" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">テンプレを使用する</a>
        </div>
        '''
        
        if i % 3 == 0:
            with col1:
                components.html(canva_embed_code + button_code, height=500)
        elif i % 3 == 1:
            with col2:
                components.html(canva_embed_code + button_code, height=500)
        else:
            with col3:
                components.html(canva_embed_code + button_code, height=500)
