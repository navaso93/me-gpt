from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import re

from langchain_core.documents import Document


STOP_WORDS = {
    'a', 'about', 'and', 'are', 'did', 'do', 'for', 'has', 'have', 'his',
    'in', 'is', 'it', 'marc', 'me', 'of', 'project', 'tell', 'the', 'to',
    'what', 'which', 'who', 'with',
}


def _content_key(document):
    return (document.page_content, document.metadata.get('source', ''))


def _lexical_candidates(vector_store, query, limit=3):
    """Find named entities and acronyms that semantic search can underweight."""
    query_terms = {
        term for term in re.findall(r"[a-z0-9]+", query.lower())
        if len(term) > 1 and term not in STOP_WORDS
    }
    if not query_terms:
        return []

    stored = vector_store.get(include=['documents', 'metadatas'])
    ranked = []
    for text, metadata in zip(stored.get('documents', []), stored.get('metadatas', [])):
        document_terms = set(re.findall(r"[a-z0-9]+", text.lower()))
        overlap = query_terms & document_terms
        if not overlap:
            continue
        coverage = len(overlap) / len(query_terms)
        if coverage < 0.5:
            continue
        exact_bonus = 1 if ' '.join(sorted(query_terms)) in text.lower() else 0
        ranked.append((coverage + exact_bonus, Document(page_content=text, metadata=metadata or {})))

    ranked.sort(key=lambda item: item[0], reverse=True)

    # If the query names a documented topic (for example "PV Dome"), return
    # every chunk from that topic and do not mix in similarly themed projects.
    normalized_query = ' '.join(re.findall(r"[a-z0-9]+", query.lower()))
    for _, document in ranked:
        topic = document.metadata.get('topic')
        normalized_topic = ' '.join(re.findall(r"[a-z0-9]+", (topic or '').lower()))
        if normalized_topic and normalized_topic in normalized_query:
            return [
                Document(page_content=text, metadata=metadata or {})
                for text, metadata in zip(stored.get('documents', []), stored.get('metadatas', []))
                if (metadata or {}).get('topic') == topic
            ]

    return [document for _, document in ranked[:limit]]

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

    lexical_docs = _lexical_candidates(vector_store, query)
    named_topic = any(document.metadata.get('topic') for document in lexical_docs)
    semantic_docs = [] if named_topic else vector_store.similarity_search(query, k=5)

    retrieved_docs = []
    seen = set()
    for document in lexical_docs + semantic_docs:
        key = _content_key(document)
        if key not in seen:
            seen.add(key)
            retrieved_docs.append(document)

    # We group the retrieved docs to create the context later in the prompt
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    return retrieved_docs, context
