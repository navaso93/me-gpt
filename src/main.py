from src.retrieval import retrieved_documents
from src.assistant import standard_prompt, job_fit_prompt, llm_answer

def answer_question(question):

    _, context = retrieved_documents(question)

    prompt = standard_prompt(question, context)

    return llm_answer(prompt, max_tokens=1000)


def job_fit(job_description):

    _, context = retrieved_documents(job_description)

    prompt = job_fit_prompt(job_description, context)

    return llm_answer(prompt, max_tokens = 1000)
