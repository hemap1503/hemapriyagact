from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa_endpoint(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda text: "Test answer")
    response = client.post("/qa", json={"text": "What is AI?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Test answer"


def test_quiz_endpoint(monkeypatch):
    sample = [
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "explanation": "2 + 2 equals 4."
        },
        {
            "question": "Which is a planet?",
            "options": ["Moon", "Mars", "Sun", "Cloud"],
            "answer": "Mars",
            "explanation": "Mars is a planet."
        },
        {
            "question": "Water freezes at?",
            "options": ["0 C", "50 C", "100 C", "200 C"],
            "answer": "0 C",
            "explanation": "Pure water freezes at 0 C under standard pressure."
        }
    ]
    monkeypatch.setattr(main, "generate_quiz", lambda text: sample)
    response = client.post("/quiz", json={"text": "Basic science"})
    assert response.status_code == 200
    assert len(response.json()["quiz"]) == 3
