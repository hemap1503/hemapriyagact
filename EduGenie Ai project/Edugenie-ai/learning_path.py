from ai_client import generate

async def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    fallback = (f"Demo learning path for {topic}:\n1. Beginner: learn the definition and prerequisites.\n"
                "2. Foundation: study core terms and simple examples.\n3. Practice: complete guided exercises.\n"
                "4. Intermediate: build a small practical task.\n5. Advanced: study deeper concepts and complete a project.\n"
                "Use your course textbook and teacher-recommended resources. Configure Gemini for a tailored plan.")
    prompt = (f"Create a practical learning roadmap for '{topic}' for a learner currently at '{level}' level. "
              "Organize beginner to advanced stages, include ordered topics, suggested practice, a realistic "
              "timeline, milestones, and resource types (do not invent exact URLs or books). Format in readable Markdown.")
    return await generate(prompt, fallback)
