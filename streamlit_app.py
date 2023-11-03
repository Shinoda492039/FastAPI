import streamlit as st
import requests

st.title('ChatGPTサンプル')

USER_NAME = 'user'
ASSISTANT_NAME = 'assistant'

# セッション状態にチャットログを初期化
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

user_msg = st.chat_input('質問を具体的に入力してください')

if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat['name']):
            st.write(chat['msg'])

    # ユーザーのメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # FastAPIバックエンドからアシスタントのレスポンスを取得
    response = requests.post('https://fastapi-o0z4.onrender.com', json={"user_msg": user_msg})
    if response.status_code == 200:
        assistant_msg = response.json()['answer']
        with st.chat_message(ASSISTANT_NAME):
            st.write(assistant_msg)
    else:
        st.error('アシスタントからのレスポンス取得中にエラーが発生しました。')

    # チャットログにメッセージを追加
    st.session_state.chat_log.append({'name': USER_NAME, 'msg': user_msg})
    st.session_state.chat_log.append({'name': ASSISTANT_NAME, 'msg': assistant_msg})
