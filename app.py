import streamlit as st

from src.main import answer_question


# Configure the page
st.set_page_config(
    page_title="Marc GPT",
    page_icon="💬",
)

st.title("Marc GPT")
st.write("Ask me about Marc's experience, projects, and skills.")


# Collect the recruiter's question
question = st.text_input("What would you like to know?")


# Generate and display the answer
if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        answer = answer_question(question)

    st.write(answer)
