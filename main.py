from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI
import openai

# ファインチューニング後のモデル
model_list = openai.FineTuningJob.list(limit=10)
fine_tuned_model_name = model_list['data'][2]['fine_tuned_model']

app = FastAPI()

# リクエストボディ定義
class Question(BaseModel):
    content: str

@app.post('/question')
def question(question: Question):
    response = openai.ChatCompletion.create(
        model = fine_tuned_model_name,
        messages = [
            {'role': 'user', 'content': question.content},
        ],
    )
    return {'answer': response.choices[0]['message']['content'].strip()}
