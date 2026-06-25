# Project Name

Web application for inventory management.

## Stack
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL
- Frontend: React + TypeScript
- Tests: pytest + Playwright

## Commands
- `make dev`: Start development server
- `make test`: Run all tests
- `make lint`: Run ruff + eslint
- `make migrate`: Run database migrations

## Architecture
- `backend/`: FastAPI application
  - `models/`: SQLAlchemy models
  - `routers/`: API endpoints
  - `services/`: Business logic
- `frontend/`: React SPA
  - `src/components/`: Reusable components
  - `src/pages/`: Route pages
  - `src/hooks/`: Custom React hooks

## Conventions
- All API endpoints return JSON
- Use Pydantic models for request/response validation
- Write tests for all new endpoints
- Use conventional commits: feat:, fix:, docs:, refactor:
- Never commit directly to main; use feature branches

## Code Style
- Python: ruff format, 88 char line length
- TypeScript: prettier, single quotes
- Use type hints everywhere in Python
- Prefer async/await over sync code
