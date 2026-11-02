import math
import sqlite3
from datetime import UTC, datetime

from app.schemas.task import TaskCreate, TaskUpdate


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
        "priority": row["priority"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "user_id": row["user_id"],
    }


def create_task(db: sqlite3.Connection, task_data: TaskCreate):
    cursor = db.execute(
        "INSERT INTO tasks (title, description, priority, user_id, created_at) VALUES (?, ?, ?, ?, ?)",
        (task_data.title, task_data.description, task_data.priority, task_data.user_id, datetime.now(UTC).isoformat()),
    )
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _row_to_dict(row)


def get_task(db: sqlite3.Connection, task_id):
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def get_tasks(db: sqlite3.Connection):
    rows = db.execute("SELECT * FROM tasks").fetchall()
    return [_row_to_dict(row) for row in rows]


def get_tasks_paginated(
    db: sqlite3.Connection,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    priority: str | None = None,
):
    # Build WHERE clause from filters
    conditions = []
    params: list = []
    if status == "pending":
        conditions.append("completed = 0")
    elif status == "completed":
        conditions.append("completed = 1")
    if priority is not None:
        conditions.append("priority = ?")
        params.append(priority)

    where_clause = (" WHERE " + " AND ".join(conditions)) if conditions else ""

    # Filtered count
    count_row = db.execute(f"SELECT COUNT(*) FROM tasks{where_clause}", params).fetchone()
    total = count_row[0]
    total_pages = max(1, math.ceil(total / page_size))

    # Clamp page to valid range
    page = min(page, total_pages)

    offset = (page - 1) * page_size
    rows = db.execute(
        f"SELECT * FROM tasks{where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?",
        params + [page_size, offset],
    ).fetchall()
    items = [_row_to_dict(row) for row in rows]

    # Global (unfiltered) stats
    stats_row = db.execute(
        "SELECT COUNT(*) as total, "
        "SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) as pending, "
        "SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed "
        "FROM tasks"
    ).fetchone()

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        },
        "stats": {
            "total": stats_row[0] or 0,
            "pending": stats_row[1] or 0,
            "completed": stats_row[2] or 0,
        },
    }


def update_task(db: sqlite3.Connection, task_id, task_data: TaskUpdate):
    existing = get_task(db, task_id)
    if not existing:
        return None
    update_fields = task_data.model_dump(exclude_unset=True)
    if not update_fields:
        return existing
    update_fields["updated_at"] = datetime.now().isoformat()
    set_clause = ", ".join(f"{k} = ?" for k in update_fields)
    values = list(update_fields.values()) + [task_id]
    db.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
    db.commit()
    return get_task(db, task_id)


def delete_task(db: sqlite3.Connection, task_id):
    existing = get_task(db, task_id)
    if not existing:
        return False
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return True


def complete_task(db: sqlite3.Connection, task_id):
    existing = get_task(db, task_id)
    if not existing:
        return None
    db.execute(
        "UPDATE tasks SET completed = 1, updated_at = ? WHERE id = ?",
        (datetime.now(UTC).isoformat(), task_id),
    )
    db.commit()
    return get_task(db, task_id)
