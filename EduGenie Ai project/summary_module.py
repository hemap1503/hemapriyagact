from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for a student.

Requirements:
- Keep the important facts and ideas.
- Remove repetition and unnecessary detail.
- Use clear, easy-to-revise language.
- Prefer short paragraphs and bullet points when useful.
- Do not add facts that are not supported by the passage.

Passage:
{text}
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, an educational summarization assistant.",
        temperature=0.2,
        max_output_tokens=1600,
    )
