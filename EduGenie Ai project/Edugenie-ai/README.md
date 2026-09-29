# EduGenie — Google Gemini Powered Learning Assistant

A small FastAPI + HTML/CSS/JavaScript learning assistant following the supplied project brief. It includes Q&A, simplified explanations, three-question MCQ quizzes, passage summaries, and beginner-to-advanced learning paths.

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection and a Google AI Studio Gemini API key for live AI answers (optional)

## Setup in VS Code (Windows)
1. Extract the `EduGenie` folder and open it in VS Code (`File → Open Folder`).
2. Open **Terminal → New Terminal** and create a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again. Or use Command Prompt: `.venv\Scripts\activate.bat`.
3. Install packages:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to a new file named `.env`. To enable Gemini, create an API key in Google AI Studio and put it after `GEMINI_API_KEY=`. Keep `.env` private; do not commit or share it. `GEMINI_MODEL` defaults to `gemini-2.5-flash`; change it only to a model enabled for your API key.
5. Start the app from the project folder:
   ```powershell
   uvicorn main:app --reload
   ```
6. Open `http://127.0.0.1:8000` in your browser. Stop the server with `Ctrl+C`.

### macOS / Linux
Create and activate with `python3 -m venv .venv` and `source .venv/bin/activate`, then install requirements and run `uvicorn main:app --reload`.

## Features and API
| Feature | Method and endpoint | JSON body |
|---|---|---|
| Q&A | `POST /qa` | `{"text":"Which is the largest ocean?"}` |
| Explain | `POST /explain` | `{"text":"Photosynthesis","level":"Beginner"}` |
| Quiz | `POST /quiz` | `{"text":"Paste a topic or passage"}` |
| Summary | `POST /summarize` | `{"text":"Paste a passage"}` |
| Learning path | `POST /learn/recommendations` | `{"text":"SQL","level":"Beginner"}` |
| Health | `GET /health` | none |
| Interactive API docs | `GET /docs` | none |

The web form sends requests to the endpoints and displays the results. The quiz interface checks selected answers and shows feedback. Inputs are limited to 12,000 characters.

## Demo mode and AI mode
Without `GEMINI_API_KEY`, the site runs in **offline demo mode** using clearly labelled generic sample responses; this confirms the frontend/backend workflow but is not topic-specific AI. With a valid key, the modules call Gemini. The project brief names Gemini 1.5 Pro; model availability can change, so the model is configurable with `GEMINI_MODEL` and defaults to `gemini-2.5-flash`. The brief also describes LaMini-Flan-T5-783M for local explanations; this starter keeps installation lightweight and uses Gemini for explanations. A local Transformers model can be added separately if required and supported by your computer.

## Testing
- Visit `/health`; expect `{"status":"ok", ...}`.
- Open `/docs` to try each POST endpoint. Supply JSON such as `{"text":"Explain the water cycle","level":"Beginner"}`.
- In the browser, test all five dropdown tasks with a short input. For quiz, select options and verify feedback appears.
- For actual generative responses, set a valid API key and restart the server. Never expose the key in frontend JavaScript or screenshots.

## Troubleshooting
- `python` not found: install Python 3.10+ and enable PATH, then reopen VS Code.
- Import errors: activate `.venv` and run `pip install -r requirements.txt` again.
- Gemini authentication/model errors: check `.env`, ensure the key is active and the model is available to your account, then restart Uvicorn.
- Port busy: run `uvicorn main:app --reload --port 8001` and open port 8001.

## Project structure
```text
EduGenie/
├── main.py
├── ai_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```
