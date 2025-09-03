# Container Accounting API

Проект на **FastAPI** с использованием **MySQL**, **SQLAlchemy (async)**, **Alembic** и **JWT-аутентификацией**.

---

## Требования

- Docker + Docker Compose
- Python 3.12 (для локального запуска с venv)

---

## Запуск через Docker

1. Скопируйте репозиторий и создайте `.env` файл

2. Соберите и запустите контейнеры: `docker compose up --build
3. Приложение будет доступно: 
    - API: http://127.0.0.1:8000
    - Swagger UI: http://127.0.0.1:8000/docs

## Миграции (Alembic)
1. Создать новую миграцию: `docker compose exec api alembic revision --autogenerate -m "init"`
2. Применить миграции: `docker compose exec api alembic upgrade head`

## Тестирование
Создание пользователя
![userregister.png](doc-images/userregister.png)
Создание пользователя с существующим именем
![userwithexistingname.png](doc-images/userwithexistingname.png)
Ошибка авторизации пользователя
![wrongpassword.png](doc-images/wrongpassword.png)
Получение списка контейнеров (первые 50)
![allcontainers.png](doc-images/allcontainers.png)
Получение списка контейнеров по номеру
![substringsearch.png](doc-images/substringsearch.png)
Получение контейнера по конкретной цене
![getbycost.png](doc-images/getbycost.png)
Получение контейнеров по диапазону цен
![getbycostrange.png](doc-images/getbycostrange.png)
Добавление контейнера
![addcontainer.png](doc-images/addcontainer.png)
Добавление контейнера с существующим номером
![containerwithexistingnumber.png](doc-images/containerwithexistingnumber.png)


## Хешированное хранение пароля в бд
![usersinbd.png](doc-images/usersinbd.png)
