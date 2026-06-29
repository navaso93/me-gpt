# Marc GPT

Marc GPT is a RAG-powered online CV.

Recruiters can ask questions about Marc's background, projects, skills, education, and interests. The app retrieves relevant information from a public Markdown knowledge base and uses an LLM to generate grounded answers.

The goal of this project is both practical and educational: to build a small but real AI product using RAG, FastAPI, Streamlit, Docker, and cloud deployment.

## Live Product Structure

Marc GPT has two main parts:

1. **Streamlit frontend**
   - Public user interface.
   - Lets users ask questions.
   - Lets users paste a job description for a job-fit evaluation.
   - Sends requests to the backend API.

2. **FastAPI backend**
   - Receives requests from Streamlit.
   - Retrieves relevant chunks from ChromaDB.
   - Builds a grounded prompt.
   - Calls Gemini.
   - Returns the answer to Streamlit.

## Current Features

- Ask recruiter-style questions about Marc.
- Evaluate whether Marc is a good fit for a pasted job description.
- Retrieve context from Markdown knowledge files.
- Use ChromaDB as the vector database.
- Use Gemini for embeddings and answer generation.
- Show answers only from Marc's provided knowledge base.
- Refuse or limit answers when the knowledge base does not contain enough information.
- Deploy the frontend with Streamlit Community Cloud.
- Deploy the API with Docker and Google Cloud Run.

## Project Structure

```text
marc-gpt/
  app.py                  # Streamlit frontend
  Dockerfile              # Docker image for the FastAPI backend
  requirements.txt
  .env.example
  .gitignore
  README.md

  knowledge/              # Public Markdown knowledge base
    profile.md
    experience.md
    projects.md
    skills.md
    education.md
    interests.md
    faq.md

  src/
    ingest.py             # Loads, splits, and embeds Markdown documents
    retrieval.py          # Retrieves relevant chunks from ChromaDB
    assistant.py          # Builds prompts and calls the LLM
    main.py               # Main app workflow functions
    api.py                # FastAPI endpoints

  tests/
    test_ingest.py
    test_retrieval.py
    test_assistant.py
    test_api.py
```

## Environment Variables

Create a local .env file:

GOOGLE_API_KEY = your_google_api_key
API_URL=http://127.0.0.1:8000

Notes:
- GOOGLE_API_KEY is used by the backend for Gemini
- API_URL is used by Streamlit to know where the FastAPI backend is.
- Never commit .env.

For Streamlit Community Cloud, set API_URL in the app secrets.
For Google Cloud Run, store GOOGLE_API_KEY in Secret Manager.

## Run locally

Create and activate a virtual environment:
```bash
 python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

Start the FastAPI backend:
```bash
uvicorn src.api:app --reload
```
In another terminal, start Streamlit:
```bash
streamlit run app.py
```

## Rebuild thevector database

After editing files in knowledge/, rerun the ingestion step so ChromaDB contains the latest information.

Example:

```bash
python -m src.ingest
```

## API Endpoints

The backend exposes "GET /" health check endpoint.

'POST /answer':
- Receives a recruiter question and returns a grounded answer.
- Expected JSON:
  {
    "question": "What experience does Marc have with NLP?"
  }

'POST /job_fit':
- Receives a job description and returns a job-fit evaluation:
- Expected JSON:
  {
    "job_description": "Paste job description here..."
  }

FastAPI docs are available locally at:
- http://127.0.0.1:8000/docs

## Tests
Run:
```bash
pytest tests/
```
The tests check:
- Markdown loading and chunking.
- Retrieval behavior using fake dependencies.
- Prompt construction.
- FastAPI endpoint availability and response format.
The tests avoid real Gemini or Chroma calls where possible, so they stay fast and do not spend API credits.

## Deployment

The frontend is deployed with Streamlit Community Cloud.
The backend is deployed separately:
1) Build a Docker image.
2) Push it to Google Artifact Registry.
3) Deploy it to Google Cloud Run.
4) Store GOOGLE_API_KEY securely in Google Secret Manager.
5) Set the Streamlit API_URL secret to the Cloud Run URL.
When only app.py changes, push to GitHub and Streamlit redeploys.
When backend code changes, rebuild and redeploy the Docker image.
When knowledge files change, rerun ingestion, rebuild the Docker image if chroma_db/ is included in it, and redeploy Cloud Run.

## Knowledge Base Guidelines

The Markdown files in knowledge/ are the source of truth.
Each section should be self-contained and include:
- Project or experience name.
- Marc's role.
- Dates when relevant.
- Responsibilities.
- Technologies used.
- Outcomes or results.
- Lessons learned.
- Public links when available.
Avoid private information, vague claims, or unsupported achievements.

## Possible next improvements
Possible next improvements:
1) Add source snippets under each answer.
2) Improve job-fit scoring and structure.
3) Add answer modes: recruiter, technical interviewer, casual.
4) Add usage analytics for common recruiter questions.
5) Add GitHub project links in generated answers.
6) Add CI tests with GitHub Actions.
7) Add basic protection or rate limiting for the public API.
