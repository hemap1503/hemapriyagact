from ai_client import generate

async def answer_question(question: str) -> str:
    fallback = ("Demo response: Start by identifying the key idea in your question, then review a "
                "trusted textbook or class note for details. Add a Gemini API key in .env to receive "
                "a topic-specific AI answer.")
    prompt = ("You are EduGenie, a careful educational tutor. Answer the learner's question clearly, "
              "accurately, and concisely. Use simple language, define important terms, and mention "
              "uncertainty rather than inventing facts.\nQuestion: " + question)
    return await generate(prompt, fallback)
