from src.assistant import GroundedAssistant, NOT_FOUND_MESSAGE
from src.ingest import Document
from src.retrieval import LexicalRetriever


def build_assistant():
    documents = [
        Document(
            title="LIAR Project",
            content="Marc built a Python preprocessing pipeline.",
            path="knowledge/projects.md",
        )
    ]
    return GroundedAssistant(LexicalRetriever(documents))


def test_answers_supported_question_with_source():
    result = build_assistant().answer("What Python work did Marc do?")

    assert "preprocessing pipeline" in result.answer
    assert result.sources[0].title == "LIAR Project"


def test_refuses_unsupported_question():
    result = build_assistant().answer("What is Marc's home address?")

    assert result.answer == NOT_FOUND_MESSAGE
    assert result.sources == []
