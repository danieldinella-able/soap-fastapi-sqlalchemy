# Repository Guidelines

## Project Structure & Module Organization
- `app/main.py`: FastAPI app startup, CORS, router.
- `app/core/`: Core modules
  - `config/settings.py`: `.env`-driven settings (Uvicorn, Postgres).
  - `managers/`: `PostgresDBManager`, `AppStateManager`.
  - `utils/`: logging, helpers.
  - `base/`: base models, enums, responses.
- `.env`: Local configuration (never commit secrets).
- `docker-compose.yml`: Local Postgres service.
- `requirements.txt`: Python dependencies.

## Build, Test, and Development Commands
- Create venv and install deps:
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Start Postgres locally:
  - `docker-compose up -d postgres`
- Run the API with reload:
  - `uvicorn app.main:app --reload`
- Run tests (pytest):
  - `pytest -q`

## Coding Style & Naming Conventions
- Follow PEP 8; use 4-space indentation and type hints.
- Naming: `snake_case` for files/vars/functions, `PascalCase` for classes, `UPPER_CASE` for constants.
- Keep modules cohesive (e.g., DB logic in `app/core/managers`, settings in `app/core/config`).
- Pydantic v2 models live in `base`; prefer explicit field types and validators.

## Testing Guidelines
- Framework: `pytest`.
- Location: create `tests/` with files named `test_*.py`.
- Style: unit tests for `utils/` and `base/`; integration tests for DB via async `sessionmaker`.
- Example: `pytest -k utils -q` runs only utility tests.

## Commit & Pull Request Guidelines
- Commits: short imperative subject (≤72 chars), details in body if needed.
  - Example: `Add Postgres async session factory`.
- Pull Requests: include scope/intent, steps to reproduce/run, env changes (e.g., new `.env` keys), and sample curl for new endpoints.
- Link related issues; include screenshots or JSON samples for API responses when relevant.

## Security & Configuration Tips
- Configure `.env` (do not commit credentials):
  - `POSTGRES_URI=postgresql+asyncpg://appuser:apppass@localhost:5432/app_test`
- Use `docker-compose` credentials for local dev only.
- Logs are JSON/colored by environment; avoid logging secrets.

## Recent Changes
- ace79ee: test.
- e5a624b: test.
- 3a2f6c6: main and db manager fix.
- cd77d1f: Docker and db setup.
- 632d594: First commit.
