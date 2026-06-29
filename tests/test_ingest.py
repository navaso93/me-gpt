from src.ingest import load_documents, split_documents
from langchain_core.documents import Document


def test_markdown_loads_correctly(tmp_path):
    knowledge_folder = tmp_path / "knowledge"
    knowledge_folder.mkdir()

    markdown_file = knowledge_folder / "profile.md"
    markdown_file.write_text("# Profile\n\n Marc is learning RAG.", encoding="utf-8")

    documents = load_documents(knowledge_folder)

    assert len(documents) == 1
    assert "Marc is learning RAG" in documents[0].page_content
    assert documents[0].metadata["source"].endswith("profile.md")

def test_doc_split_into_chunks():

    long_text = "Marc worked with Python and SQL and RAG." * 100

    documents = [
        Document(
            page_content=f"# Profile\n\n## Projects \n\n{long_text}",
            metadata={'source':"profile.md"}
        )
    ]

    chunks = split_documents(documents)

    assert len(chunks) > 1
    assert all(chunk.page_content for chunk in chunks)
    assert all(chunk.metadata["source"] == "profile.md" for chunk in chunks)
