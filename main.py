from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI
import openai

app = FastAPI()

# リクエストボディ定義
class Question(BaseModel):
    content: str

@app.post("/question")
def question(question: Question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question.content},
        ],
    )
    return {"answer": response.choices[0]["message"]["content"].strip()}
