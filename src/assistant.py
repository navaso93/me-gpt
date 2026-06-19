from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model


def generate_prompt(query, context):
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
