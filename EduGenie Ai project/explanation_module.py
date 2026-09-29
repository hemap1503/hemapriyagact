import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def _local_pipeline():
    """
    Loads the LaMini-Flan-T5 model only when the local explainer is enabled.
    The first use may download the model from Hugging Face.
    """
    from transformers import pipeline

    model_name = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline(
        "text2text-generation",
        model=model_name,
        tokenizer=model_name,
        device=-1,
    )


def _local_explain(topic: str) -> str:
    generator = _local_pipeline()
    prompt = (
        "Explain this topic to a beginner in simple, concise educational language. "
        "Use a short definition, key points, and one simple example.\n\n"
        f"Topic: {topic}"
    )
    result = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False,
    )
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    """
    Primary behavior follows the project document: LaMini-Flan-T5 is used
    for concept explanation. If local inference is disabled or unavailable,
    EduGenie falls back to Gemini so the web application remains usable.
    """
    use_local = os.getenv("USE_LOCAL_EXPLAINER", "true").lower() in {
        "1", "true", "yes", "on"
    }

    if use_local:
        try:
            return _local_explain(topic)
        except Exception as local_error:
            # Keep the service usable when a local model cannot be loaded.
            from gemini_client import generate_text
            fallback_prompt = f"""
Explain the topic "{topic}" to a beginner.
Use simple language, a short definition, key points, and one simple example.
Do not invent facts.
"""
            result = generate_text(
                fallback_prompt,
                system_instruction="You are EduGenie, an educational concept explainer.",
                temperature=0.3,
                max_output_tokens=1000,
            )
            return f"{result}\n\n(Local explainer unavailable; Gemini fallback was used.)"

    from gemini_client import generate_text
    return generate_text(
        f"Explain this topic simply for a student:\n{topic}",
        system_instruction="You are EduGenie, an educational concept explainer.",
        temperature=0.3,
        max_output_tokens=1000,
    )
