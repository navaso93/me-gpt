from src.ingest import Document
from src.retrieval import LexicalRetriever


def test_retrieval_ranks_matching_document_first():
    documents = [
        Document("NLP Project", "Python classification with RoBERTa.", "projects.md"),
        Document("Cooking", "Bread and soup.", "interests.md"),
    ]

    results = LexicalRetriever(documents).search("RoBERTa classification")

    assert results[0].document.title == "NLP Project"
