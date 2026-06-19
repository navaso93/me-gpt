from src.retrieval import retrieved_documents
from src.assistant import generate_prompt, llm_answer

def answer_question(question):

    _, context = retrieved_documents(question)

    prompt = generate_prompt(question, context)

    return llm_answer(prompt, max_tokens=1000)
