import base64
import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


# Configuration
load_dotenv()

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

PROFILE_IMAGE = Path("assets/profile.jpg")
BACKGROUND_IMAGE = Path("assets/sunset_clouds.jpg")


# Page setup
st.set_page_config(
    page_title="Marc GPT",
    page_icon="💬",
    layout="wide",
)


# Visual styling
def apply_style():
    background = """
        background:
            radial-gradient(circle at top left, #dbeafe, transparent 35%),
            linear-gradient(135deg, #f8fafc, #eef2ff);
    """

    # Base64 converts the image into text that CSS can embed directly.
    if BACKGROUND_IMAGE.exists():
        encoded = base64.b64encode(
            BACKGROUND_IMAGE.read_bytes()
        ).decode()

        background = f"""
            background:
                linear-gradient(rgba(253,241,229,1), rgba(253,241,229,1)),
                url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        """

    st.markdown(
        f"""
        <style>
        .stApp {{ {background} }}
        .block-container {{
            max-width: 1100px;
            padding-top: 2rem;
        }}
        .avatar {{
            width: 210px;
            height: 210px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: linear-gradient(135deg, #4f46e5, #06b6d4);
            color: white;
            font-size: 4rem;
            font-weight: 700;
            margin: auto;
        }}
        .tag {{
            display: inline-block;
            padding: .35rem .75rem;
            margin: .2rem;
            border-radius: 999px;
            background: #ffe2bc;
            color: #ff9e10;
            font-size: .85rem;
            font-weight: 600;
        }}
        div[data-testid="stForm"] {{
            background: rgba(255,255,255,.82);
            padding: 1.4rem;
            border-radius: 18px;
            border: 1px solid #e2e8f0;
        }}
        .profile-frame img {{
            margin-top: 30px;
            margin-left: 30px;
            width: 220px;
            height: 220px;
            object-fit: cover;
            border-radius: 50%;
            border: 1px solid #000000;
        }}
        .profile-links {{
            margin-top: 1rem;
            text-align: center;
        }}
        .profile-links a {{
            display: inline-block;
            margin: 0.25rem;
            padding: 0.45rem 0.75rem;
            border-radius: 999px;
            background: #fff7ed;
            color: #ea580c !important;
            text-decoration: none;
            font-weight: 600;
            border: 1px solid #fed7aa;
        }}
        .profile-links a:hover {{
            background: #ffedd5;
        }}
        html, body, .stApp {{
            color: #111827 !important;
        }}

        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {{
            color: #111827 !important;
        }}

        h1, h2, h3, h4 {{
            color: #111827 !important;
        }}

        label, .stTextInput label, .stTextArea label {{
            color: #111827 !important;
        }}

        div[data-testid="stForm"] {{
            background: rgba(255,255,255,.92) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_style()


# API communication
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

    except requests.HTTPError:
        st.error(f"The API returned error {response.status_code}.")

    except requests.ConnectionError:
        st.error("Marc GPT could not connect to the API.")

    return None

# Hero section
with st.container():
    image_column, text_column = st.columns([1, 2], gap="large")

    with image_column:
        if PROFILE_IMAGE.exists():
            image_base64 = base64.b64encode(PROFILE_IMAGE.read_bytes()).decode()

            st.markdown(
                f"""
                <div class="profile-frame">
                    <img src="data:image/jpeg;base64,{image_base64}">
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="avatar">MN</div>', unsafe_allow_html=True)
            st.caption("Add assets/profile.jpg")
        st.markdown(
            """
            <div class="profile-links">
                <a href="https://github.com/navaso93" target="_blank">GitHub</a>
                <a href="https://linkedin.com/in/marc-navarro-sotés/" target="_blank">LinkedIn</a>
                <a href="mailto:mnavarrosotes@gmail.com">Email</a>
                <a href="https://app.notion.com/p/Portfolio-Marc-Navarro-386a73a4ed5280efa99bd47efb571508">Portfolio</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with text_column:
        st.markdown('<div class="hero">', unsafe_allow_html=True)
        st.title("Hi, I'm Marc!")
        st.subheader("And this is my AI recruitment assistant: Marc GPT")
        st.write(
            "Marc GPT knows everything about my career, and of course some basic personal information that can also be relevant for career purposes.  \n\n"
            "Ask anything about my profile, experience, or skills, and it will give you all the information you need. "
            "\nYou can also paste a full job description and see how it fits my profile, and then"
            " get a score and a compatibility breakdown."
        )
        st.markdown("</div>", unsafe_allow_html=True)


st.write("")
ask_tab, fit_tab = st.tabs(["💬Open question", "🎯Evaluate Job Fit"])


# Standard recruiter questions
with ask_tab:
    st.subheader("Ask about Marc")
    st.write("Ask about projects, education, skills or professional experience.")

    with st.form("question_form"):
        question = st.text_input(
            "Your question",
            placeholder="What experience does Marc have with RAG?",
        )
        ask_button = st.form_submit_button(
            "Ask Marc-GPT",
            use_container_width=True,
        )

    if ask_button:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching Marc's profile..."):
                answer = call_api("answer", {"question": question})

            if answer:
                with st.container(border=True):
                    st.subheader("Marc GPT")
                    st.write(answer)


# Job-fit evaluation
with fit_tab:
    st.subheader("Evaluate job fit")
    st.write(
        "Paste a job description to compare its requirements with evidence "
        "from Marc's professional profile."
    )

    with st.form("job_fit_form"):
        job_description = st.text_area(
            "Job description",
            placeholder="Paste the complete job description here...",
            height=300,
        )
        evaluate_button = st.form_submit_button(
            "Evaluate job fit",
            use_container_width=True,
        )

    if evaluate_button:
        if not job_description.strip():
            st.warning("Please paste a job description.")
        else:
            with st.spinner("Comparing the role with Marc's profile..."):
                fit_answer = call_api(
                    "job_fit",
                    {"job_description": job_description},
                )

            if fit_answer:
                with st.container(border=True):
                    st.subheader("Job-fit assessment")
                    st.write(fit_answer)


# Footer
st.divider()
st.caption(
    "Marc GPT generates answers from Marc's public knowledge base. "
    "Job-fit assessments are informational and do not replace an interview."
)
