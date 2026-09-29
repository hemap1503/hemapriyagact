from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()
app = FastAPI(title="EduGenie", version="1.0.0", description="AI-powered learning assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TextRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=12000)
    level: str = Field(default="Beginner", max_length=40)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": "EduGenie"})

async def run_task(task, payload: TextRequest):
    text = payload.text.strip()
    if len(text) < 2:
        raise HTTPException(status_code=422, detail="Please enter a topic, question, or passage.")
    try:
        if task == "qa": result = await answer_question(text)
        elif task == "explain": result = await explain_concept(text, payload.level)
        elif task == "quiz": result = await generate_quiz(text)
        elif task == "summarize": result = await summarize_text(text)
        else: result = await get_learning_recommendations(text, payload.level)
        return {"task": task, "result": result, "mode": "AI" if os.getenv("GEMINI_API_KEY") else "offline demo"}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"EduGenie could not complete this request: {exc}") from exc

@app.post("/qa")
async def qa(payload: TextRequest): return await run_task("qa", payload)
@app.post("/explain")
async def explain(payload: TextRequest): return await run_task("explain", payload)
@app.post("/quiz")
async def quiz(payload: TextRequest): return await run_task("quiz", payload)
@app.post("/summarize")
async def summarize(payload: TextRequest): return await run_task("summarize", payload)
@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest): return await run_task("learn", payload)

@app.get("/health")
async def health():
    return {"status": "ok", "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))}
