from ai_client import generate

async def summarize_text(content: str) -> str:
    fallback = ("Demo summary: This passage should be reviewed for its central idea, supporting points, "
                "and conclusion. Add a Gemini API key to generate a summary of the supplied passage.")
    prompt = ("Summarize the following educational passage in clear, simple language. Preserve its main "
              "facts and meaning, remove repetition, and do not add information. Use a short paragraph "
              "followed by key points when useful.\nPASSAGE:\n" + content)
    return await generate(prompt, fallback)
