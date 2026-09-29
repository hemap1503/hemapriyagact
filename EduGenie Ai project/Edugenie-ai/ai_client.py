"""Shared Gemini client. Without an API key, modules return local demo responses."""
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def get_client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    from google import genai
    return genai.Client(api_key=key)

async def generate(prompt: str, fallback: str) -> str:
    client = get_client()
    if client is None:
        return fallback
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response. Try again.")
    return text.strip()
