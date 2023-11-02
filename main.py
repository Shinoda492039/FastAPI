from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI
import openai

# インスタンス化
app = FastAPI()

# 入力するデータ型の定義
class Question(BaseModel):
    content: str

# 学習済みのモデルの読み込み
model_list = openai.FineTuningJob.list(limit=10)
fine_tuned_model_name = model_list['data'][2]['fine_tuned_model']

# POST が送信された時（入力）と予測値（出力）の定義
@app.post('/question')
def question(question: Question):
    response = openai.ChatCompletion.create(
        model = fine_tuned_model_name,
        messages = [
            {'role': 'user', 'content': question.content},
        ],
    )
    return {'answer': response.choices[0]['message']['content'].strip()}
