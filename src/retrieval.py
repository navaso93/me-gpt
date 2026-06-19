from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

def retrieved_documents(query):

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    embeddings = GoogleGenerativeAIEmbeddings(
        model='models/gemini-embedding-001',
        api_key=api_key
    )

    vector_store = Chroma(
        collection_name='marc_gpt',
        embedding_function=embeddings,
        persist_directory='./chroma_db'
    )

    retrieved_docs = vector_store.similarity_search(query, k=5)

    # We group the retrieved docs to create the context later in the prompt
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    return retrieved_docs, context
