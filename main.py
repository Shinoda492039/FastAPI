from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# FastAPIアプリケーションの初期化
app = FastAPI()

# 学習済みのモデルの読み込み
model_list = openai.FineTuningJob.list(limit=10)
fine_tuned_model_name = model_list['data'][2]['fine_tuned_model']

# POSTリクエスト用のモデル
class UserMessage(BaseModel):
    user_msg: str

# ChatGPTからのレスポンスを取得するためのエンドポイント
@app.post('/question')
async def get_chatgpt_response(user_message: UserMessage):
    try:
        response = openai.ChatCompletion.create(
            model=fine_tuned_model_name,
            messages=[
                {'role': 'user', 'content': user_message.user_msg},
            ],
            stream=True
        )
        # レスポンスのチャンクを蓄積
        assistant_msg = ''.join(chunk['choices'][0]['delta'].get('content', '') for chunk in response)
        return {"answer": assistant_msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))