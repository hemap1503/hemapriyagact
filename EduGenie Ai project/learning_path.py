from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for the topic: "{topic}".

Structure it as:
1. Beginner foundations
2. Intermediate concepts
3. Advanced concepts
4. Practice/projects
5. Suggested learning resources

For each stage, give a short description and practical next steps.
Include a reasonable sequence rather than an overwhelming list.
When suggesting resources, name useful resource types or well-known educational resources,
but do not fabricate URLs, course names, prices, or claims about availability.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, a structured learning-path advisor.",
        temperature=0.5,
        max_output_tokens=2200,
    )
