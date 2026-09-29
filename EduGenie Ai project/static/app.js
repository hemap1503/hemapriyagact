const form = document.getElementById("eduForm");
const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const submitButton = document.getElementById("submitButton");
const buttonText = document.getElementById("buttonText");
const spinner = document.getElementById("spinner");
const copyButton = document.getElementById("copyButton");

const placeholders = {
    qa: "Example: Which is the largest ocean?",
    explain: "Example: Explain photosynthesis for a beginner.",
    quiz: "Paste a passage here to generate 3 MCQs.",
    summarize: "Paste a long educational passage here.",
    learn: "Example: SQL"
};

task.addEventListener("change", () => {
    inputText.placeholder = placeholders[task.value];
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = inputText.value.trim();
    if (!text) return;

    setLoading(true);
    resultCard.classList.remove("hidden");
    result.innerHTML = "";

    try {
        const endpoint = endpointFor(task.value);
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "The server returned an error.");
        }

        if (task.value === "quiz") {
            renderQuiz(data.quiz);
        } else if (task.value === "learn") {
            renderText(data.recommendations);
        } else if (task.value === "explain") {
            renderText(data.explanation);
        } else if (task.value === "summarize") {
            renderText(data.summary);
        } else {
            renderText(data.answer);
        }
    } catch (error) {
        result.innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
    } finally {
        setLoading(false);
    }
});

copyButton.addEventListener("click", async () => {
    const text = result.innerText.trim();
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        copyButton.textContent = "Copied!";
        setTimeout(() => copyButton.textContent = "Copy", 1200);
    } catch {
        copyButton.textContent = "Copy failed";
        setTimeout(() => copyButton.textContent = "Copy", 1200);
    }
});

function endpointFor(value) {
    return {
        qa: "/qa",
        explain: "/explain",
        quiz: "/quiz",
        summarize: "/summarize",
        learn: "/learn/recommendations"
    }[value];
}

function setLoading(loading) {
    submitButton.disabled = loading;
    buttonText.textContent = loading ? "Working..." : "Get Result";
    spinner.classList.toggle("hidden", !loading);
}

function renderText(text) {
    result.textContent = text;
}

function renderQuiz(quiz) {
    result.innerHTML = "";

    quiz.forEach((item, index) => {
        const box = document.createElement("div");
        box.className = "quiz-question";

        const heading = document.createElement("h3");
        heading.textContent = `${index + 1}. ${item.question}`;
        box.appendChild(heading);

        item.options.forEach((option) => {
            const button = document.createElement("button");
            button.className = "option-button";
            button.type = "button";
            button.textContent = option;

            button.addEventListener("click", () => {
                const allOptions = box.querySelectorAll(".option-button");
                allOptions.forEach((btn) => btn.disabled = true);

                const feedback = document.createElement("div");
                feedback.className = "feedback";

                if (option === item.answer) {
                    feedback.classList.add("correct");
                    feedback.textContent = `Correct! ${item.explanation || ""}`;
                } else {
                    feedback.classList.add("wrong");
                    feedback.textContent =
                        `Not quite. Correct answer: ${item.answer}. ${item.explanation || ""}`;
                }

                box.appendChild(feedback);
            });

            box.appendChild(button);
        });

        result.appendChild(box);
    });
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}
