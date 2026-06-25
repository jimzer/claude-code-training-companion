# Code Style Rules

## Python
- Use ruff for formatting and linting
- Line length: 88 characters
- Use `from __future__ import annotations` in all files
- Prefer `pathlib.Path` over `os.path`
- Use dataclasses or Pydantic models, never raw dicts for structured data
- All functions must have return type annotations
- Use `typing.Final` for constants

## Naming
- Files: snake_case.py
- Classes: PascalCase
- Functions/variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Private methods: _leading_underscore
- Test files: test_<module>.py

## Imports
- Group: stdlib, third-party, local (separated by blank lines)
- Use absolute imports, never relative
- No wildcard imports (`from x import *`)
