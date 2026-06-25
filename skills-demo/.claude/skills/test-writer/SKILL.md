---
description: Generates pytest tests for the specified module or function
user-invocable: true
---

# Test Writer Skill

When invoked with `/test-writer`, generate comprehensive pytest tests.

## Instructions
1. Read the target file/function
2. Identify all code paths (happy path, edge cases, error cases)
3. Generate tests using pytest style
4. Use fixtures from conftest.py if available
5. Follow the example pattern below

## Conventions
- One test function per behavior
- Use descriptive names: `test_<function>_<scenario>_<expected>`
- Use `pytest.raises` for error cases
- Group related tests in classes

## Example
See `examples/sample_test.py` for the expected test style.
