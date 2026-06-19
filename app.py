import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# API address:
# Locally, FastAPI runs on port 8000.
# In production, API_URL will contain the Cloud Run address.
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)


# Configure the Streamlit page
st.set_page_config(
    page_title="Marc GPT",
    page_icon="💬",
)

st.title("Marc GPT")
st.write("Ask about Marc's experience, projects, and skills.")


# Collect the user's question
question = st.text_input("What would you like to know?")


# Send the question to FastAPI
if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"{API_URL}/answer",
                json={"question": question},
                timeout=60,
            )

            # Raise an error if FastAPI returned an error status
            response.raise_for_status()

            # Extract "answer" from the returned JSON
            answer = response.json()["answer"]

            st.write(answer)

        except requests.RequestException:
            st.error("The API could not be reached.")
