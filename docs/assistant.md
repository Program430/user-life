# Userlife assistant

## Product idea

Userlife is a personal assistant that stores durable life information and helps turn a message into a useful answer or a proposed action. A phone client can call the HTTP API; a frontend or messenger integration is intentionally not included yet.

## Core entities

- `notes` — free-form thoughts and information;
- `tasks` — reminders and things to do, with optional person and due date;
- `debts` — amount, currency, direction, person, due date and status;
- `events` — appointments and plans with start/end time and location;
- `ideas` — ideas that should not be lost;
- `assistant_messages` — short conversation history used for context.

Each concept has its own table because its lifecycle and fields are different. There is no generic `life_items` table and no document database at this stage.

## API

Health:

- `GET /health`
- `GET /health/db`

Life entities support simple create/list operations:

- `POST|GET /api/v1/notes`
- `POST|GET /api/v1/tasks`
- `POST|GET /api/v1/debts`
- `POST|GET /api/v1/events`
- `POST|GET /api/v1/ideas`

Assistant:

- `POST /api/v1/assistant/ask` with `{ "message": "..." }`;
- `GET /api/v1/assistant/messages` for recent conversation history.

The assistant returns a human-readable `reply` and structured `actions`. Actions are drafts: the application does not silently create a debt, task or event from an LLM response. Confirmation and action application can be added later without changing the provider layer.

## Free model strategy

The provider chain is configured with `LLM_PROVIDERS` and tries providers in order:

1. `ollama` — local model, no API billing;
2. `gemini` — Google AI Studio free tier, subject to current model and rate limits;
3. `openrouter` — uses `openrouter/free`, which routes to an available free model.

The first available provider wins. A provider failure moves the request to the next provider. No paid model is selected by the defaults.

Ollama is the safest local default:

```bash
ollama pull llama3.2:3b
```

For a hosted free option, set one of the API keys and keep the corresponding provider in `LLM_PROVIDERS`:

```env
LLM_ENABLED=true
LLM_PROVIDERS=gemini,openrouter
LLM_GEMINI_API_KEY=replace-me
LLM_GEMINI_MODEL=gemini-2.5-flash
LLM_OPENROUTER_API_KEY=replace-me
LLM_OPENROUTER_MODEL=openrouter/free
```

Free tiers have quotas and can change. The provider name, model and order are environment variables so the application does not need a code change when a free model is replaced.

## Migration

The first real migration creates the core tables:

```bash
docker compose up --build -d
docker compose exec app poetry run alembic upgrade head
```

Do not use `Base.metadata.create_all()` at application startup. Production applies migrations from GitHub Actions before the Render Deploy Hook.

## Important next step

Before exposing the API publicly, add authentication or a private gateway. The current MVP is intentionally single-user and has no auth layer.
