# userlife

Минимальный production-style backend на FastAPI с асинхронным SQLAlchemy и PostgreSQL.

## Architecture

Код использует простой поток зависимостей:

```text
HTTP route -> application service -> repository -> PostgreSQL
```

Слои находятся в `src/userlife`:

- `presentation` — FastAPI routes и зависимости;
- `application` — сервисы;
- `infrastructure` — SQLAlchemy, PostgreSQL и repositories;
- `core` — настройки и logging.

`GET /health` не зависит от базы. `GET /health/db` выполняет `SELECT 1` и возвращает `503`, если база недоступна.

## Local development

Требования: Docker Desktop и Poetry.

```bash
cp .env.example .env
poetry install
docker compose up --build
```

Проверки:

```text
http://localhost:8000/health
http://localhost:8000/health/db
```

## Environment variables

- `APP_ENV` — окружение, по умолчанию `development`;
- `APP_NAME` — имя приложения;
- `LOG_LEVEL` — уровень logging, по умолчанию `INFO`;
- `PORT` — HTTP-порт, по умолчанию `8000`;
- `DATABASE_URL` — PostgreSQL URL.

Локальный URL:

```text
postgresql+psycopg://postgres:postgres@db:5432/userlife
```

Production URL Supabase передаётся через environment variable. Если URL начинается с `postgresql://` или `postgres://`, приложение нормализует его для async psycopg автоматически.

## Database migrations

Миграций пока нет, потому что таблиц приложения ещё нет. Alembic уже настроен на metadata SQLAlchemy и готов к первой миграции.

После добавления модели:

```bash
poetry run alembic revision --autogenerate -m "add notes"
poetry run alembic upgrade head
```

В Docker Compose:

```bash
docker compose exec app poetry run alembic revision --autogenerate -m "add notes"
docker compose exec app poetry run alembic upgrade head
```

Миграции не запускаются автоматически при старте приложения.

## Docker

Production Dockerfile использует Python 3.12 slim, Poetry без виртуального окружения внутри контейнера и запускает:

```bash
uvicorn userlife.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Git flow

Разработка ведётся в `develop`. В `main` попадают готовые изменения через merge или PR. Только push в `main` запускает production workflow.

## Production deployment

Production рассчитан на Render Web Service с Docker runtime:

- branch: `main`;
- Auto Deploy: `OFF`;
- Health Check Path: `/health`;
- environment variables: `DATABASE_URL`, `APP_ENV=production`, `LOG_LEVEL=INFO`.

Render собирает Dockerfile самостоятельно. GitHub Actions сначала применяет миграции к Supabase, а затем вызывает Render Deploy Hook.

## Render setup

1. Создайте Render Web Service из GitHub-репозитория.
2. Выберите Docker runtime и ветку `main`.
3. Отключите Auto Deploy.
4. Укажите Health Check Path `/health`.
5. Добавьте `DATABASE_URL`, `APP_ENV=production` и `LOG_LEVEL=INFO`.
6. Создайте Deploy Hook и сохраните его URL в GitHub Secret `RENDER_DEPLOY_HOOK`.

## GitHub Actions setup

Добавьте в GitHub Secrets:

- `DATABASE_URL` — production Supabase connection string;
- `RENDER_DEPLOY_HOOK` — URL Render Deploy Hook.

Workflow `.github/workflows/deploy.yml` запускается только после push в `main` и не выполняет Docker build.

## CI and production deploy workflow

`.github/workflows/ci.yml` runs on pushes to `develop` and pull requests into `main`. It installs the locked Poetry dependencies, runs existing tests if any, and runs Ruff. It does not use production secrets, connect to Supabase, run migrations, or call Render.

`.github/workflows/deploy.yml` runs only on pushes to `main`. It runs tests if present, applies `alembic upgrade head` with the `DATABASE_URL` GitHub Secret, and calls the Render Deploy Hook only after all previous steps succeed. It never builds a Docker image in GitHub Actions; Render builds the Dockerfile.

Production deploys use a concurrency group with `cancel-in-progress: false`, so migrations cannot run in parallel for two pushes to `main`.

## Supabase setup

Создайте PostgreSQL project в Supabase и используйте Session Pooler connection string для IPv4. Передайте этот URL в Render и GitHub Secret `DATABASE_URL`. Supabase SDK не требуется: приложение работает с Supabase как с обычным PostgreSQL через SQLAlchemy.

## Personal assistant domain

The current domain includes notes, tasks/reminders, debts, events, ideas and assistant message history. The entity model and assistant API are documented in [docs/assistant.md](docs/assistant.md).

The assistant uses a configurable free-provider chain: local Ollama first, then Gemini free tier and OpenRouter `openrouter/free`. Provider keys and model names are environment variables. LLM actions are returned as drafts and are not written to financial or calendar data without a future confirmation step.
