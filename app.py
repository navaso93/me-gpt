import streamlit as st

from src.assistant import GroundedAssistant
from src.ingest import load_knowledge
from src.retrieval import LexicalRetriever


st.set_page_config(page_title="Marc GPT", page_icon="M", layout="centered")


@st.cache_resource
def build_assistant() -> GroundedAssistant:
    documents = load_knowledge("knowledge")
    return GroundedAssistant(LexicalRetriever(documents))


assistant = build_assistant()

st.title("Marc GPT")
st.caption("Ask about Marc's projects, skills, education, and experience.")

with st.sidebar:
    st.header("Try asking")
    st.markdown(
        "- What did Marc contribute to the LIAR project?\n"
        "- Which NLP technologies has Marc used?\n"
        "- What is Marc still learning?"
    )
    st.info(
        "Answers are grounded only in Marc's public knowledge base. "
        "The app will say when it cannot answer."
    )

question = st.chat_input("Ask a recruiter-style question")
if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        result = assistant.answer(question)
        st.write(result.answer)
        if result.sources:
            st.markdown("**Sources**")
            for source in result.sources:
                label = f"{source.title} ({source.path})"
                if source.url:
                    st.markdown(f"- [{label}]({source.url})")
                else:
                    st.markdown(f"- {label}")
