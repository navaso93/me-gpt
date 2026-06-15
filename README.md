# Marc GPT

Marc GPT is a small RAG-style online CV. Recruiters can ask questions about Marc and
receive answers grounded only in a public Markdown knowledge base, with supporting
sources shown beneath each answer.

## MVP scope

The first version deliberately favors clarity and deployability over infrastructure:

1. Structured Markdown is the source of truth.
2. A small local BM25-style retriever finds relevant sections.
3. If `OPENAI_API_KEY` is configured, OpenAI writes a concise grounded answer.
4. Without an API key, the app returns relevant source excerpts, so it still works.
5. Unsupported questions receive an explicit "not enough information" response.

ChromaDB and semantic embeddings are a sensible next milestone after the content and
answer behavior have been validated with real recruiter questions.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Optionally copy `.env.example` to `.env`, set `OPENAI_API_KEY`, and load those variables
in your shell or deployment environment. Never commit the key.

## Test

```powershell
pytest
```

## Content design

Edit files in `knowledge/`. Each level-two heading becomes a retrievable section.
Sections should stand alone and explicitly include Marc's role, contribution,
technologies, outcomes, dates, and relevant public links. Do not add private details.

Before publishing, Marc should replace all placeholder "not yet added" sections with
either verified public facts or remove those sections.

## Small next milestones

1. Test ten real recruiter questions and improve the Markdown content.
2. Add ChromaDB plus semantic embeddings behind the existing retriever boundary.
3. Add automated groundedness and refusal tests.
4. Deploy to Streamlit Community Cloud.
