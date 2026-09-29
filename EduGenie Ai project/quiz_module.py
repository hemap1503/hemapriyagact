import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data: Any) -> list[dict]:
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON list.")

    if len(data) != 3:
        raise ValueError("Quiz response must contain exactly three questions.")

    validated = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is not an object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must have four options.")
        options = [str(option).strip() for option in options]

        if not answer or answer not in options:
            raise ValueError(
                f"Question {index} must have an answer matching one option."
            )

        validated.append({
            "question": question,
            "options": options,
            "answer": answer,
            "explanation": explanation,
        })

    return validated


def generate_quiz(passage: str) -> list[dict]:
    prompt = f"""
Create exactly three multiple-choice questions from the educational passage below.

Return ONLY valid JSON. No Markdown fences and no extra text.

JSON format:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Exactly one option from the options array",
    "explanation": "Brief explanation of why the answer is correct"
  }}
]

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- Only one correct answer.
- Questions must be answerable from the passage.
- Distractors should be plausible but incorrect.
- Keep the language student-friendly.

Passage:
{passage}
"""
    raw = generate_text(
        prompt,
        system_instruction="You generate strictly structured educational quiz JSON.",
        temperature=0.4,
        max_output_tokens=1800,
    )

    try:
        data = json.loads(clean_json_block(raw))
        return _validate_quiz(data)
    except (json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"Quiz generation/parsing failed: {exc}") from exc
