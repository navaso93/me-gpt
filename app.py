import os

import requests
import streamlit as st
from dotenv import load_dotenv


# Load local environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# Configure the browser page
st.set_page_config(
    page_title="Marc GPT",
    page_icon="💬",
    layout="centered",
)


# Reusable function for calling FastAPI
def call_api(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}/{endpoint}",
            json=payload,
            timeout=300,
        )
        response.raise_for_status()
        return response.json()["answer"]

    except requests.Timeout:
        st.error("The request took too long. Please try again.")

    except requests.RequestException:
        st.error("The API encountered an error.")

    return None


# Sidebar information
with st.sidebar:
    st.header("About Marc GPT")
    st.write(
        "Marc GPT answers recruiter questions using information "
        "from Marc's public professional knowledge base."
    )

    st.divider()

    st.subheader("Example questions")
    st.write("- What projects has Marc completed?")
    st.write("- Which technologies has Marc used?")
    st.write("- What did Marc contribute to the LIAR project?")

    st.info("Answers may be incomplete when information is unavailable.")


# Main page introduction
st.title("Marc GPT")
st.caption("An AI-powered interactive CV")

st.write(
    "Ask about Marc's experience, projects, education, "
    "skills, or professional interests."
)

st.divider()


# Standard recruiter question
st.subheader("Ask about Marc")

with st.form("question_form"):
    question = st.text_input(
        "Your question",
        placeholder="For example: What experience does Marc have with NLP?",
    )

    ask_button = st.form_submit_button("Ask Marc GPT")

if ask_button and question:
    with st.spinner("Searching Marc's profile..."):
        answer = call_api(
            endpoint="answer",
            payload={"question": question},
        )

    if answer:
        st.success("Answer")
        st.write(answer)


st.divider()


# Optional job-fit analysis
evaluate_job_fit = st.checkbox("Evaluate job fit for Marc")

if evaluate_job_fit:
    st.subheader("Job-fit evaluation")

    st.write(
        "Paste a job description below. Marc GPT will compare its "
        "requirements with evidence from Marc's professional profile."
    )

    with st.form("job_fit_form"):
        job_description = st.text_area(
            "Job description",
            placeholder="Paste the complete job description here...",
            height=250,
        )

        evaluate_button = st.form_submit_button("Evaluate job fit")

    if evaluate_button and job_description:
        with st.spinner("Comparing the role with Marc's profile..."):
            fit_answer = call_api(
                endpoint="job_fit",
                payload={"job_description": job_description},
            )

        if fit_answer:
            st.success("Job-fit evaluation")
            st.write(fit_answer)


# Editable footer
st.divider()
st.caption(
    "Marc GPT provides an AI-generated assessment grounded in Marc's "
    "public profile. It should not replace a personal interview."
)
