from fastapi.testclient import TestClient

from src import api


client = TestClient(api.app)


def test_api_has_expected_routes():
    # app.routes contains all FastAPI endpoints registered with decorators.
    routes = [route.path for route in api.app.routes]

    assert "/" in routes
    assert "/answer" in routes
    assert "/job_fit" in routes


def test_root_endpoint_returns_status():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Marc GPT API is running"


def test_answer_endpoint_returns_answer(monkeypatch):
    # Replace the real RAG function so the test does not call Chroma/Gemini.
    def fake_answer_question(question):
        return f"Fake answer for: {question}"

    monkeypatch.setattr(api, "answer_question", fake_answer_question)

    response = client.post(
        "/answer",
        json={"question": "What projects has Marc done?"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Fake answer for: What projects has Marc done?"


def test_job_fit_endpoint_returns_answer(monkeypatch):
    # Replace the real job-fit function so the test stays fast and local.
    def fake_job_fit(job_description):
        return f"Fake job fit for: {job_description}"

    monkeypatch.setattr(api, "job_fit", fake_job_fit)

    response = client.post(
        "/job_fit",
        json={"job_description": "Python data scientist role"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Fake job fit for: Python data scientist role"
