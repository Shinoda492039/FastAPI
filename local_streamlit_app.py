import streamlit as st
import openai
import requests
import os

# ローカル環境用 API キー
openai.api_key = os.environ['OPENAI_API_KEY']

# 学習済みのモデルの読み込み
model_list = openai.FineTuningJob.list(limit=10)
fine_tuned_model_name = model_list['data'][2]['fine_tuned_model']

# フロント構成コード

# 予測の実行
#     response = requests.post('http://localhost:8000/question', json = input_text)
#     prediction = response.json()['answer']

st.title('ChatGPTサンプル')

# 定数定義
USER_NAME = 'user'
ASSISTANT_NAME = 'assistant'

def response_chatgpt(
    user_msg: str,
):
    """ChatGPTのレスポンスを取得

    Args:
        user_msg (str): ユーザーメッセージ。
    """
    response = openai.ChatCompletion.create(
        model = fine_tuned_model_name,
        messages = [
            {'role': 'user', 'content': user_msg},
        ],
        stream=True
    )
    return response

# チャットログを保存したセッション情報を初期化
if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

user_msg = st.chat_input('質問を具体的に入力してください')
if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat['name']):
            st.write(chat['msg'])

    # 最新のメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    response = response_chatgpt(user_msg)
    with st.chat_message(ASSISTANT_NAME):
        assistant_msg = ''
        assistant_response_area = st.empty()
        for chunk in response:
            # 回答を逐次表示
            tmp_assistant_msg = chunk['choices'][0]['delta'].get('content', '')
            assistant_msg += tmp_assistant_msg
            assistant_response_area.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({'name': USER_NAME, 'msg': user_msg})
    st.session_state.chat_log.append({'name': ASSISTANT_NAME, 'msg': assistant_msg})
