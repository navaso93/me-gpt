import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.main import answer_question, job_fit



# Create the API application
app = FastAPI()

# Keep the original Streamlit client working while allowing the standalone web
# frontend to use the same public API. Set ALLOWED_ORIGINS to a comma-separated
# list in production to restrict browser access to known frontend domains.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials="*" not in allowed_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


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
