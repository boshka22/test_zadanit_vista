<div align="center">

# 📝 Diary API

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Чистая архитектура, асинхронность, лучшие практики**

</div>

## 📋 О проекте

Backend-приложение для ведения ежедневника с возможностью создания, редактирования и отслеживания задач. 
Построено на принципах чистой архитектуры с четким разделением на слои.

## ✨ Возможности

- ✅ **CRUD операции** — полный цикл работы с записями
- 🔍 **Фильтрация** — по статусу выполнения (completed/active)
- 📄 **Пагинация** — удобная навигация по списку записей
- 🏷️ **Отметка выполнения** — специальный эндпоинт для смены статуса
- 🐳 **Docker поддержка** — легкий запуск в контейнерах

## 🛠 Технологический стек

| Компонент | Технология |
|-----------|------------|
| **Язык** | Python 3.12 |
| **Фреймворк** | FastAPI |
| **База данных** | PostgreSQL 16 |
| **ORM** | SQLAlchemy 2.0 (asyncio) |
| **Миграции** | Alembic |
| **Валидация** | Pydantic / pydantic-settings |
| **Линтеры** | flake8, black, isort, mypy |
| **Тестирование** | pytest, pytest-asyncio, httpx |
| **Контейнеризация** | Docker, docker-compose |

## 📁 Структура проекта

```
diary-api/
├── app/
│   ├── api/                    # HTTP слой
│   │   └── v1/
│   │       ├── router.py       # Корневой роутер
│   │       └── routes/
│   │           └── entries.py  # Эндпоинты записей
│   ├── services/               # Бизнес-логика
│   │   └── entries.py
│   ├── repository/             # Работа с данными
│   │   ├── base.py
│   │   └── entries.py
│   ├── database/               # Модели и подключение
│   │   ├── base.py
│   │   ├── models/
│   │   │   └── entry.py
│   │   └── session.py
│   ├── config/                 # Конфигурация
│   │   └── settings.py
│   └── main.py                 # Точка входа
├── alembic/                     # Миграции
├── tests/                       # Тесты
├── .env.example                 # Пример конфигурации
├── docker-compose.yml           # Docker Compose
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🚀 Быстрый старт

### Вариант 1: Локальный запуск

1. **Клонировать репозиторий**
```bash
git clone https://github.com/yourusername/diary-api.git
cd diary-api
```

2. **Создать виртуальное окружение**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

3. **Установить зависимости**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Настроить окружение**
```bash
cp .env.example .env
# Отредактировать .env, указав свои параметры БД
```

5. **Создать базу данных**
```bash
createdb diary_db
# или через psql: CREATE DATABASE diary_db;
```

6. **Применить миграции**
```bash
alembic upgrade head
```

7. **Запустить приложение**
```bash
uvicorn app.main:app --reload
```

### Вариант 2: Запуск через Docker

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

## 📡 API Эндпоинты

Базовый префикс: `/api/v1`

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/entries/` | Создать запись |
| GET | `/entries/{id}` | Получить запись по ID |
| GET | `/entries/` | Список записей (с пагинацией и фильтрацией) |
| PUT | `/entries/{id}` | Обновить запись |
| DELETE | `/entries/{id}` | Удалить запись |
| POST | `/entries/{id}/complete` | Отметить как выполненную |

### Примеры запросов

#### 📝 Создание записи
```bash
curl -X POST "http://localhost:8000/api/v1/entries/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Встреча с командой",
    "content": "Обсуждение архитектуры",
    "event_time": "15:30:00"
  }'
```

#### 📋 Получение списка с фильтрацией
```bash
# Только выполненные записи, первые 10
curl "http://localhost:8000/api/v1/entries/?completed_only=true&skip=0&limit=10"
```

#### ✅ Отметка выполнения
```bash
curl -X POST "http://localhost:8000/api/v1/entries/1/complete"
```

## 🔧 Качество кода

```bash
# Форматирование
black app tests
isort app tests

# Линтинг
flake8
mypy app
```

## 📄 Лицензия

MIT License. Подробнее в файле [LICENSE](LICENSE).

