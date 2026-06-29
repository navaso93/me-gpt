from src.assistant import standard_prompt


def test_generate_prompt_includes_question_and_context():
    # This is fake retrieved context, like the text coming from Chroma.
    context = "Marc built a RAG project using Python, ChromaDB, and Gemini."

    # This is the recruiter/user question.
    question = "What experience does Marc have with RAG?"

    prompt = standard_prompt(question, context)

    # Convert to string so the test works whether your prompt is a string,
    # a LangChain message object, or a list of messages.
    prompt_text = str(prompt)

    assert question in prompt_text
    assert context in prompt_text


def test_generate_prompt_contains_grounding_instruction():
    context = "Marc used Python in the LIAR project."
    question = "Should I hire Marc?"

    prompt = standard_prompt(question, context)
    prompt_text = str(prompt).lower()

    # The assistant should be told not to invent information.
    assert "do not invent" in prompt_text or "only" in prompt_text
