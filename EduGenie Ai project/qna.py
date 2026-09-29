from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, an educational assistant.

Answer the student's question below accurately and clearly.
- Use simple language.
- Be concise but complete.
- If the question is ambiguous, state the assumption you used.
- For calculations, show the important steps.
- Do not invent citations or claim to have browsed the web.

Student question:
{question}
"""
    return generate_text(
        prompt,
        system_instruction="You are a helpful, age-appropriate educational tutor.",
        temperature=0.3,
        max_output_tokens=1200,
    )
