import json, re
from ai_client import generate

def clean_json_block(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s*```$", "", raw)
    start, end = raw.find("["), raw.rfind("]")
    if start >= 0 and end > start: return raw[start:end+1]
    return raw

async def generate_quiz(content: str):
    fallback = [{"question":"What is the best first step when studying a new topic?","options":["Memorize without context","Understand the key idea","Skip examples","Avoid questions"],"answer":"Understand the key idea","explanation":"Understanding the main idea helps connect details."},
                {"question":"Which activity helps check understanding?","options":["Self-testing","Only rereading titles","Ignoring mistakes","Skipping practice"],"answer":"Self-testing","explanation":"Questions reveal what you understand and what needs review."},
                {"question":"What should you do when a concept is unclear?","options":["Give up","Guess every time","Review an explanation and example","Avoid the topic"],"answer":"Review an explanation and example","explanation":"A clear explanation and worked example can help."}]
    prompt = ("Create exactly 3 educational multiple-choice questions based on the input. Each has exactly "
              "4 options and one correct answer. Return ONLY valid JSON array, schema: [{\"question\":str,"
              "\"options\":[str,str,str,str],\"answer\":str,\"explanation\":str}]. The answer must exactly "
              "match one option.\nINPUT:\n" + content)
    raw = await generate(prompt, json.dumps(fallback))
    try:
        data = json.loads(clean_json_block(raw))
        if not isinstance(data, list) or len(data) != 3: raise ValueError("Expected exactly 3 questions")
        for q in data:
            if not isinstance(q.get("question"), str) or len(q.get("options", [])) != 4 or q.get("answer") not in q["options"]:
                raise ValueError("Quiz format invalid")
        return data
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not parse quiz response: {exc}") from exc
