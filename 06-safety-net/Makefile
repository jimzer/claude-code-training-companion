.PHONY: format lint typecheck test check

# Mutating helpers (run by hand while developing)
format:
	uv run ruff format .

# The gate: non-mutating, fails loudly. This is what the Stop hook and CI run.
check:
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy app.py
	uv run pytest -q
