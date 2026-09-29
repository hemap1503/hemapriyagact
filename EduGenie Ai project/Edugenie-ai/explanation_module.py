from ai_client import generate

async def explain_concept(topic: str, level: str = "Beginner") -> str:
    fallback = (f"Demo explanation for {topic}: Think of this as a concept to learn in small steps. "
                "First understand its basic definition, then identify its main parts, and finally "
                "work through a simple example. Configure GEMINI_API_KEY for a tailored explanation.")
    prompt = (f"Explain '{topic}' to a {level} learner. Use simple language, a short definition, "
              "3-5 key points, one everyday or academic example, and a brief recap. Avoid unsupported claims.")
    return await generate(prompt, fallback)
