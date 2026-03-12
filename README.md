## Diary API

Небольшое backend-приложение-ежедневник на **Python + FastAPI + PostgreSQL** с использованием чистой архитектуры (слои `api`, `services`, `repository`, `database`, `config` и др.).

Поддерживаемые операции над записями ежедневника:

- **создание записи** (например, «Тренировка в 15:00»);
- **чтение записи** по ID;
- **просмотр списка записей**;
- **редактирование записи**;
- **удаление записи**;
- **пометка записи как отработанной**.

### Технологический стек

- **Python 3.12**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (asyncio)**, **Alembic**
- **pydantic / pydantic-settings**
- **flake8**, **black**, **isort**, **mypy**
- **Docker**, **docker-compose**

---

### Структура проекта (основное)

- `app/`
  - `main.py` — точка входа FastAPI-приложения.
  - `api/` — HTTP-слой (маршруты, роутеры).
    - `v1/router.py` — корневой роутер v1.
    - `v1/routes/entries.py` — эндпоинты для записей ежедневника.
  - `services/`
    - `entries.py` — бизнес-логика по работе с записями.
  - `repository/`
    - `base.py` — базовый репозиторий.
    - `entries.py` — репозиторий для записей ежедневника.
  - `database/`
    - `base.py` — базовый класс моделей SQLAlchemy.
    - `models/entry.py` — модель записи ежедневника.
    - `session.py` — создание `AsyncEngine` и `AsyncSession`.
  - `config/`
    - `settings.py` — конфигурация приложения (pydantic-settings).
- `alembic/` — миграции базы данных.
  - `env.py` — настройка Alembic.
  - `versions/0001_create_entries_table.py` — первичная миграция.
- `alembic.ini` — конфигурация Alembic.
- `Dockerfile`, `docker-compose.yml` — Docker-окружение.
- `.flake8`, `pyproject.toml`, `mypy.ini` — настройки линтеров/форматтеров/типизации.
- `requirements.txt` — зависимости проекта.

---

### Настройка окружения (локально, без Docker)

1. **Создать и активировать виртуальное окружение**:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
```

2. **Установить зависимости**:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Создать файл `.env`** в корне проекта:

```env
DATABASE_URL=postgresql+asyncpg://diary_user:diary_password@localhost:5432/diary_db
```

4. **Создать базу данных PostgreSQL** (пример для psql):

```bash
createdb diary_db
createuser diary_user --pwprompt
# задать пароль diary_password и выдать нужные права (createdb не обязателен)
```

5. **Применить миграции Alembic**:

```bash
alembic upgrade head
```

6. **Запустить приложение**:

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`, а документация Swagger — по адресу `http://127.0.0.1:8000/docs`.

---

### Запуск с помощью Docker

1. Убедитесь, что установлены **Docker** и **docker-compose**.

2. В корне проекта выполните:

```bash
docker-compose up --build
```

Это поднимет:

- контейнер `diary-postgres` с PostgreSQL;
- контейнер `diary-app` с приложением FastAPI.

Приложение по умолчанию доступно по `http://localhost:8000`.

Чтобы остановить контейнеры:

```bash
docker-compose down
```

---

### Основные эндпоинты

Базовый префикс API: `/api/v1`.

- **POST** `/api/v1/entries/` — создание записи.
- **GET** `/api/v1/entries/{entry_id}` — получение записи по ID.
- **GET** `/api/v1/entries/` — список всех записей.
- **PUT** `/api/v1/entries/{entry_id}` — обновление записи.
- **DELETE** `/api/v1/entries/{entry_id}` — удаление записи.
- **POST** `/api/v1/entries/{entry_id}/complete` — пометить запись как отработанную.

Полная интерактивная документация доступна в Swagger UI (`/docs`) и ReDoc (`/redoc`).

---

### Проверки качества кода

- **black** (форматирование):

```bash
black app
```

- **isort** (импорты):

```bash
isort app
```

- **flake8** (линтер):

```bash
flake8
```

- **mypy** (проверка типов):

```bash
mypy app
```

---

### Примечания по архитектуре

- **api-слой** содержит только HTTP-специфичную логику (маршруты, валидация входа/выхода через Pydantic-схемы).
- **services-слой** инкапсулирует бизнес-логику (создание, обновление, удаление, получение, пометка записей).
- **repository-слой** отвечает за доступ к данным (SQLAlchemy, запросы к БД).
- **database-слой** содержит модели и настройки подключения к PostgreSQL.
- **config-слой** управляет конфигурацией приложения и переменными окружения.

