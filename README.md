# Message Broker Demo

Простое Python-приложение с RabbitMQ:
- `producer` (папка `producer/`) периодически отправляет задачи (арифметические операции) в exchange `tasks`.
- `consumer` (папка `consumer/`) обрабатывает задачи, подтверждает успешные и отклоняет ошибки в DLQ.
- Общий код в `common/`. Docker Compose поднимает отдельные образы для producer и consumer плюс RabbitMQ (UI `:15672`).

## Запуск
```bash
docker compose up --build
```
- RabbitMQ UI: http://localhost:15672 (guest/guest).
- Producer логирует отправку, Consumer — обработку. Ошибочные сообщения попадают в очередь `tasks.dlq`.

## Фоновый запуск и просмотр логов
```bash
docker-compose up -d --build
docker compose logs producer
docker compose logs consumer
```

## Переменные окружения
- `RABBITMQ_HOST` (default `rabbitmq`)
- `RABBITMQ_PORT` (default `5672`)
- `ROUTING_KEY` (default `math`)
- `PUBLISH_INTERVAL` (producer, default `3`)
- `PREFETCH_COUNT` (consumer, default `10`)

## Тесты и статический анализ
```bash
pip install -r requirements.txt
pytest
flake8 .
```

## Очистка

```bash
docker compose down
docker image prune -a
```

## CI/CD (GitHub Actions)
- Workflow: `.github/workflows/ci.yml`
- Jobs: `lint-test` (flake8 + pytest) и `docker` (build + push в GHCR с `GITHUB_TOKEN`).
- Имя образа: `ghcr.io/<owner>/<repo>/message-broker:latest`.

## Структура
- `app/operations.py` — бизнес-логика вычислений.
- `app/producer.py` — генерация сообщений.
- `app/consumer.py` — потребитель с DLQ.
- `docker-compose.yml` — сервисы RabbitMQ + приложения.

