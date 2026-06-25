from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

items = {}

class Item(BaseModel):
    name: str
    price: float
    quantity: int = 0

@app.get("/items")
def list_items():
    return list(items.values())

@app.post("/items")
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = {"id": item_id, **item.model_dump()}
    return items[item_id]

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # No error handling -- intentional gap
    del items[item_id]
    return {"deleted": True}

@app.get("/health")
def health():
    return {"status": "ok", "items_count": len(items)}
