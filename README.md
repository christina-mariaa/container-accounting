# Container Accounting API

Проект на **FastAPI** с использованием **MySQL**, **SQLAlchemy (async)**, **Alembic** и **JWT-аутентификацией**.

---

## Требования

- Docker + Docker Compose
- Python 3.12 (для локального запуска с venv)

---

## Запуск через Docker

1. Скопируй репозиторий и создай `.env` файл:

2. Собери и запусти контейнеры: `docker compose up --build
3. Приложение будет доступно: 
    - API: http://127.0.0.1:8000
    - Swagger UI: http://127.0.0.1:8000/docs

## Миграции (Alembic)
1. Создать новую миграцию: `docker compose exec api alembic revision --autogenerate -m "init"`
2. Применить миграции: `docker compose exec api alembic upgrade head`
