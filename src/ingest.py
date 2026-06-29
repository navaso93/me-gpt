from pathlib import Path
from dotenv import load_dotenv
import os
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings



def load_documents(knowledge_path="knowledge"):

    documents = []

    for file_path in Path(knowledge_path).glob('*.md'):
        text = file_path.read_text(encoding='utf-8')

        documents.append(
            Document(
                page_content=text,
                metadata={'source':str(file_path)}
            )
        )
    return documents



def split_documents(documents):
    # "#" represents heading level 1.
    # "##" represents heading level 2.
    headers = [
        ('#','category'),
        ('##','section')
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers,
        strip_headers=False
    )

    sections = []

    for document in documents:
        file_sections = markdown_splitter.split_text(document.page_content)

        for section in file_sections:
            section.metadata['source'] = document.metadata['source']

        sections.extend(file_sections)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = text_splitter.split_documents(sections)

    return chunks



def embed_documents(chunks):

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing")

    embeddings = GoogleGenerativeAIEmbeddings(
        model='models/gemini-embedding-001',
        api_key=api_key
    )

    vector_store = Chroma(
        collection_name='marc_gpt',
        embedding_function=embeddings,
        persist_directory='./chroma_db'
    )

    document_ids = vector_store.add_documents(documents=chunks)

    return document_ids


# Run the complete ingestion process from the terminal
if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    document_ids = embed_documents(chunks)

    print(f"Embedded {len(document_ids)} chunks.")
