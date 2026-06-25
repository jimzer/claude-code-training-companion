---
description: Enforces API conventions when editing Python API files
paths: "**/*.py"
---

# API Conventions

When editing Python API files, ensure:

1. **Response models**: Every endpoint should have a `response_model` parameter
2. **Status codes**: POST endpoints return 201, DELETE returns 204
3. **Error handling**: All endpoints that access resources must handle not-found cases
4. **Docstrings**: Every endpoint function needs a one-line docstring
5. **Path naming**: Use plural nouns for collections (e.g., `/items` not `/item`)

## Example
```python
@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    """Create a new item."""
    ...
```
