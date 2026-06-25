# Enterprise Project

# Rules live in .claude/rules/ and load automatically (no import needed):
#   code-style.md  applies everywhere (no `paths:` field)
#   security.md    is path-scoped, loads only for services/ and libs/ code
# Importing them with @ would inline both unconditionally and defeat the scoping.

## Project Overview
Large-scale microservices platform for financial data processing.

## Stack
- Services: Python 3.12 + FastAPI
- Message Queue: RabbitMQ
- Database: PostgreSQL 16 + Redis
- Infrastructure: Kubernetes + Terraform
- CI/CD: GitHub Actions

## Commands
- `make dev` -- Start local dev environment (docker-compose)
- `make test` -- Run full test suite
- `make test-unit` -- Unit tests only
- `make test-integration` -- Integration tests (requires Docker)
- `make lint` -- Run all linters
- `make typecheck` -- Run mypy strict mode
- `make migrate` -- Run Alembic migrations
- `make proto` -- Generate protobuf stubs

## Architecture
- `services/` -- Individual microservices
  - Each service has its own `Dockerfile`, `pyproject.toml`, and `tests/`
- `libs/` -- Shared libraries (auth, logging, telemetry)
- `proto/` -- Protobuf definitions
- `infra/` -- Terraform modules
- `scripts/` -- CI/CD and deployment scripts

## Conventions
- All services follow hexagonal architecture
- Domain logic must never import from infrastructure layer
- Every public function requires type hints and docstrings
- Minimum 80% test coverage enforced in CI
- All database queries go through repository pattern
- Use structured logging (JSON format) everywhere
- Feature flags via LaunchDarkly for all new features

## PR Requirements
- At least 2 approvals required
- CI must pass (tests, lint, typecheck, security scan)
- No TODO comments in production code
- Changelog entry required for user-facing changes
