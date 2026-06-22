from fastapi import FastAPI
from pydantic import BaseModel

from src.main import answer_question, job_fit



# Create the API application
app = FastAPI()


# Define the expected request body
class QuestionRequest(BaseModel):
    question: str

class JobDescriptionFit(BaseModel):
    job_description: str


# Simple endpoint used to check whether the API is running
@app.get("/")
def root():
    return {"status": "Marc GPT API is running"}


# Endpoint that receives a question and returns an answer
@app.post("/answer")
def answer(request: QuestionRequest):
    result = answer_question(request.question)

    return {"answer": result}

# Endpoint that retrieves a job_description and returns a job_fit evaluation
@app.post("/job_fit")
def job_fit_comment(request: JobDescriptionFit):
    job_fit_answer = job_fit(request.job_description)

    return {"answer": job_fit_answer}
