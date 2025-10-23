# MSTUCA_LR1
Лабораторная работа №1 "Освоение Docker и Docker Compose"
# Create a README.md file in /mnt/data with the requested content.
readme_content = """# Лабораторная работа №1 — Flask + PostgreSQL в Docker Compose (Вариант 1: REST API задач)

## Цель
Освоить контейнеризацию и развертывание мультисервисного стенда с помощью Docker Compose. Реализовать REST-API на Flask с подключением к PostgreSQL, обеспечить корректные HTTP-коды, healthcheck и сохранность данных через именованный том.

## Состав стенда
- **web** — Flask-приложение (Python), REST-API по задачам (CRUD), маршрут `/health`.
- **db** — PostgreSQL, данные вынесены в именованный том `postgres_data`.
- Сервисы связаны через общую сеть Compose; строка подключения задаётся переменной окружения `DATABASE_URL`.

## Предварительные требования
- Docker + Docker Compose (CLI v2).
- Python не обязателен на хосте (всё внутри контейнеров).

## Быстрый старт
```bash
# Клонирование проекта
git clone <URL репозитория>
cd MSTUCA_LR1

# Сборка и запуск
docker compose up --build

# API будет доступно на:
# http://localhost:5000
# Health: http://localhost:5000/health
