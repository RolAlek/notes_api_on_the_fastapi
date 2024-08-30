# notes_api_on_the_fastapi
Небольшой API-клиент для создания заметок. Реализована система пользователей и разграничения доступа:
* создавать заметки может только зарегистрированный и аутентифицированный пользователь;
* пользователь может просматривать только свои заметки.

Также в приложение интегрирован spell-checker `Yandex Spellchecker` для проверки орфографии в полях `name` и `text` при создании заметки.

И все это крутится в докер-контейнерах, что позволяет развернуть приложение в одну команду.

## Стек:
* Python 3.12,
* Fastapi 0.112.2,
* SQLAlchemy 2.0.32
* PostgreSQL + asyncpg
* Alembic 1.13.2
* FastAPI-Users 13.0.0
* Docker и Docker-compose

## Установка и настройка:
* Клоинрутйе репозиторий;
* В корне проекта создайте `.env` файл и заполните его в соответсвии с `.env.example`:
```
POSTGRES_USER=ваше пользователь от ДБ
POSTGRES_PASSWORD=ваш пароль от ДБ
POSTGRES_DB=notes

APP__DB__URL=postgresql+asyncpg://pg_user:pg_password@db:5432/notes
APP__DB__ECHO=0
APP__SECRET=ваша_секретная_фраза
APP__SPELL__URL=https://speller.yandex.net/services/spellservice.json/checkText
APP__APP_NAME=Notes API application
APP__SOCKET__HOST=0.0.0.0
APP__SOCKET__PORT=8000
APP__SOCKET__POOL_SIZE=30
APP__SOCKET__MAX_OVERFLOW=10
```
### Docker:
В корне проекта выполните команду:

```sh
docker compose up
```

Перейдите по адресу `http://0.0.0.0:8000/docs` и... И все - создавайте заметки и радуйтесь!

### Для разработки:
Установите менеджер зависимостей poetry:
```sh
pip install poetry
```
Установите зависимости:
```sh
poetry install
```
Активируйте виртуальное окружение:
```sh
poetry shell
```
Запустите приложение и перейдите по адресу `http://127.0.0.1:8000/docs` для ознакомления с документацией к API и тестирования эндпоинтов.
```sh
uvicorn main:main_app
```

## Регистрация нового пользователя:
POST
http://0.0.0.0:8000/api/auth/register/:

Request:
```json
{
    "email": "user@example.com",
    "password": "userpassword"
}
```

Response:
```json
{
  "id": 0,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
POST
http://0.0.0.0:8000/api/auth/jwt/login/:
Предварительно определите `Content-type` как `x-www-form-urlencoded`...
Request
```json
{
    "email": "user@example.com",
    "password": "userpassword"
}
```
Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
  "token_type": "bearer"
}
```
POST
http://0.0.0.0:8000/api/notes/

Request
```json
{
    "name": "string",
    "text": "string"
}

Response

{
  "name": "string",
  "text": "string",
  "id": 1
}
```

GET
http://0.0.0.0:8000/api/notes/my/ - обращение авторизованного пользователя к эндпоинту вернет список всех заметок пользователя.

Response body
Download
```json
[
    {
        "name": "Саша и шоссе",
        "text": "Шагала саша по шоссе и сосала сушку",
        "id": 1
    }
    ...
]
```