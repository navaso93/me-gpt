from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model


def standard_prompt(query, context):
    # We create the prompt_template and then the prompt
    client = Client()

    system_msg = """
    Answer from the provided context.
    Do not invent information.
    If the answer is unavailable, say so clearly.
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', system_msg),
        ('human', f"""
    Context:
    {context}

    Question:
    {query}
    """),
    ])

    # We define the prompt
    prompt = prompt_template.invoke(
        {"context": context, "question": query}
    ).to_messages()

    return prompt


def job_fit_prompt(job_description, context):

    client = Client()

    system_msg = """
    Explain why Marc can be a good fit (or not) to the entered job description based on the available context.
    When giving arguments, always try to provide an example if available to back the argument.
    When you don't know something or are not sure, just say you are not sure. Do not invent.
    Give:
        - Fit score
        - Strengths
        - Gaps
        - Recommendation
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', system_msg),
        ('human', f"""
    Retrieved info on Marc similar to Job Description:
    {context}

    Job Description for Marc:
    {job_description}
    """),
    ])

    # We define the prompt
    prompt_job_fit = prompt_template.invoke(
        {"context": context, "question": job_description}
    ).to_messages()

    return prompt_job_fit


def llm_answer(prompt, max_tokens=1000):

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = init_chat_model(
        "gemini-2.5-flash-lite",
        model_provider="google_genai",
        api_key=api_key,
        max_tokens=1_000)

    answer = llm.invoke(prompt)

    return answer.content
