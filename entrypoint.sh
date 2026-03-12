#!/usr/bin/env sh
set -e

# Применяем миграции перед запуском приложения
alembic upgrade head

exec "$@"

