# Demo App

FastAPI task management API with SQLite backend.

## Stack
- FastAPI + Uvicorn
- SQLite (stdlib sqlite3)
- Pydantic v2 for schemas
- SQLite database (./tasks.db)

## Commands
- `make run`: start dev server on port 8000
- `make test`: run pytest
- `make lint`: ruff check
- `make format`: ruff format

## Architecture
- `app/`: application code
  - `models/`: data model documentation
  - `schemas/`: Pydantic request/response schemas
  - `routers/`: FastAPI route handlers
  - `services/`: Business logic layer
- `tests/`: pytest tests

## Conventions
- Services handle business logic, routers handle HTTP
- All timestamps should be UTC (NOTE: there may be a bug here)
