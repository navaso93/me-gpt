from fastapi import FastAPI
from pydantic import BaseModel

from src.main import answer_question



# Create the API application
app = FastAPI()


# Define the expected request body
class QuestionRequest(BaseModel):
    question: str


# Simple endpoint used to check whether the API is running
@app.get("/")
def root():
    return {"status": "Marc GPT API is running"}


# Endpoint that receives a question and returns an answer
@app.post("/answer")
def answer(request: QuestionRequest):
    result = answer_question(request.question)

    return {"answer": result}
