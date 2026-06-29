from langchain_core.documents import Document

from src import retrieval


class FakeEmbeddings:
    # Fake embeddings object so the test does not call Google.
    def __init__(self, *args, **kwargs):
        pass


class FakeChroma:
    # Fake Chroma vector store so the test does not use the real chroma_db.
    def __init__(self, *args, **kwargs):
        pass

    def similarity_search(self, query, k=5):
        # This simulates Chroma returning relevant documents.
        return [
            Document(
                page_content="Marc worked on NLP and RAG using Python.",
                metadata={"source": "knowledge/projects.md"},
            )
        ]


def test_retrieved_documents_returns_docs_and_context(monkeypatch):
    # Set fake API key so the function passes its environment check.
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-key")

    # Replace real external tools with fake versions.
    monkeypatch.setattr(retrieval, "GoogleGenerativeAIEmbeddings", FakeEmbeddings)
    monkeypatch.setattr(retrieval, "Chroma", FakeChroma)

    retrieved_docs, context = retrieval.retrieved_documents("What RAG work has Marc done?")

    assert len(retrieved_docs) == 1
    assert "NLP and RAG" in context
    assert retrieved_docs[0].metadata["source"] == "knowledge/projects.md"
