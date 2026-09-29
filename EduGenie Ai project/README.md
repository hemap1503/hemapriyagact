# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project document. It provides:

- Q&A
- Simplified concept explanations
- 3-question MCQ quiz generation
- Passage summarization
- Beginner-to-advanced learning recommendations
- A responsive HTML/CSS/JavaScript frontend
- FastAPI REST endpoints

## Architecture

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_api.py
```

## 1. Install Python

Use Python 3.10 or newer.

Verify:

```powershell
python --version
```

## 2. Open the project in VS Code

Open the `EduGenie` folder.

## 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the project with the venv Python directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> `torch` and `transformers` make the local LaMini-Flan-T5 explanation module substantially larger than the other dependencies.

## 5. Add your Gemini API key

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

with your actual key.

Never commit `.env` or share your API key.

## 6. Run EduGenie

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 7. Test the application

Try:

### Ask a question
`Which is the largest ocean?`

### Explain
`Pythagoras theorem`

### Quiz
Paste a short educational paragraph.

### Summarize
Paste a longer passage.

### Learning path
`SQL`

## API endpoints

- `POST /qa`
- `POST /explain`
- `POST /quiz`
- `POST /summarize`
- `POST /learn/recommendations`
- `GET /health`

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Local explanation model

The project document specifies LaMini-Flan-T5-783M for concept explanation. This implementation tries that model first when:

```text
USE_LOCAL_EXPLAINER=true
```

The first explanation request may download the model. If local loading fails, the application falls back to Gemini so the application can still respond.

If you want Gemini-only explanations, set:

```text
USE_LOCAL_EXPLAINER=false
```

## Testing

Run:

```powershell
pytest
```

The tests mock AI calls, so they do not consume Gemini API quota.

## Troubleshooting

### `GEMINI_API_KEY is missing`
Make sure `.env` exists in the project root and contains a valid key.

### PowerShell says scripts are disabled
Use:

```powershell
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

### Port 8000 is busy
Use another port:

```powershell
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

### Local explanation model is slow
Set `USE_LOCAL_EXPLAINER=false` in `.env` and restart the server.

## Source alignment

The supplied document describes FastAPI, HTML/CSS, Gemini for Q&A/quiz/summary/learning paths, and LaMini-Flan-T5 for concept explanation. This implementation preserves those functional modules while using the current Google GenAI Python SDK and a configurable Gemini model.
