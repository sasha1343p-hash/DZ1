const lead = document.getElementById("lead");
const form = document.getElementById("survey");
const status = document.getElementById("status");
const thanks = document.getElementById("thanks");

function showError(message) {
  status.textContent = message;
}

async function loadQuestions() {
  const response = await fetch("/questions");
  if (!response.ok) {
    throw new Error("Сервер не отдал список вопросов");
  }

  const data = await response.json();
  const questions = data.questions;
  if (!Array.isArray(questions) || questions.length === 0) {
    throw new Error("Список вопросов пуст");
  }

  form.replaceChildren();
  for (const question of questions) {
    const field = document.createElement("label");
    field.className = "field";
    field.htmlFor = `q-${question.id}`;
    field.textContent = question.text;

    const input = document.createElement("input");
    input.id = `q-${question.id}`;
    input.name = String(question.id);
    input.type = "text";
    input.required = true;
    input.autocomplete = "off";

    field.append(input);
    form.append(field);
  }

  const button = document.createElement("button");
  button.type = "submit";
  button.textContent = "Отправить";
  form.append(button);

  lead.textContent = "Ответьте на вопросы и отправьте форму.";
  form.hidden = false;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("");

  const answers = [...form.querySelectorAll("input")].map((input) => ({
    question_id: Number(input.name),
    value: input.value.trim(),
  }));

  const button = form.querySelector("button");
  button.disabled = true;

  try {
    const response = await fetch("/answers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers }),
    });

    if (!response.ok) {
      showError("Не удалось отправить ответы. Проверьте поля и попробуйте ещё раз.");
      button.disabled = false;
      return;
    }

    form.hidden = true;
    lead.hidden = true;
    thanks.hidden = false;
  } catch {
    showError("Нет связи с сервером. Запустите backend и обновите страницу.");
    button.disabled = false;
  }
});

loadQuestions().catch(() => {
  lead.textContent = "Не удалось загрузить вопросы.";
  showError("Проверьте, что сервер запущен, и обновите страницу.");
});
