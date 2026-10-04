FROM python:3.12-slim

ENV POETRY_VERSION=2.3.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only main --no-root --no-interaction --no-ansi

COPY src ./src
COPY alembic.ini ./
COPY alembic ./alembic
RUN poetry install --only main --no-interaction --no-ansi

EXPOSE 8000

CMD ["sh", "-c", "uvicorn userlife.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
