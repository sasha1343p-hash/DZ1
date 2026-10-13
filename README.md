# Мини-анкета

Тестовый стенд для домашнего задания: форма из нескольких вопросов. Backend отдаёт вопросы и принимает ответы, frontend показывает форму и сообщение «Спасибо!».

Ответы хранятся в списке в памяти процесса. После остановки сервера они пропадают.

## Запуск

Нужен Docker. Из корня репозитория:

```powershell
docker compose up --build
```

Откройте [http://127.0.0.1:8000](http://127.0.0.1:8000). Остановка — `Ctrl+C`.

### Без Docker

Нужен Python 3.11+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

## Эндпоинты

`GET /questions` — пять жёстко заданных вопросов.

`POST /answers` — сохранить ответы.

```json
{
  "answers": [
    {"question_id": 1, "value": "Анна"},
    {"question_id": 2, "value": "Учусь"}
  ]
}
```

Ответ: `{"status": "ok", "id": 1}`. Поле `id` — номер записи в памяти, он растёт с каждой отправкой.
