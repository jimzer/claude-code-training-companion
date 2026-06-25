.PHONY: run test lint format

run:
	uv run uvicorn app.main:app --reload --port 8000

test:
	uv run pytest -v

lint:
	uv run ruff check .

format:
	uv run ruff format .
