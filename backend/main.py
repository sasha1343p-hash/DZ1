from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

QUESTIONS = [
    {"id": 1, "text": "Как вас зовут?"},
    {"id": 2, "text": "Чем вы занимаетесь сейчас?"},
    {"id": 3, "text": "Был ли у вас опыт с нейросетями или машинным обучением?"},
    {"id": 4, "text": "Какой формат обучения вам удобнее: видео, текст или практика?"},
    {"id": 5, "text": "Что для вас будет хорошим результатом этого курса?"},
]

# Память процесса: после перезапуска сервера ответы пропадают.
ANSWERS: list[dict] = []

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="Мини-анкета")


class AnswerItem(BaseModel):
    question_id: int
    value: str

    @field_validator("value")
    @classmethod
    def value_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Ответ не может быть пустым")
        return stripped


class AnswersIn(BaseModel):
    answers: list[AnswerItem] = Field(min_length=1)


@app.get("/questions")
def get_questions() -> dict:
    return {"questions": QUESTIONS}


@app.post("/answers")
def post_answers(payload: AnswersIn) -> dict:
    known_ids = {question["id"] for question in QUESTIONS}
    seen: set[int] = set()

    for item in payload.answers:
        if item.question_id not in known_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Неизвестный вопрос: {item.question_id}",
            )
        if item.question_id in seen:
            raise HTTPException(
                status_code=400,
                detail=f"Вопрос {item.question_id} передан дважды",
            )
        seen.add(item.question_id)

    record = {
        "id": len(ANSWERS) + 1,
        "answers": [
            {"question_id": item.question_id, "value": item.value}
            for item in payload.answers
        ],
    }
    ANSWERS.append(record)
    return {"status": "ok", "id": record["id"]}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
