import sqlite3
from datetime import UTC, datetime

from app.schemas.user import UserCreate


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
        "created_at": row["created_at"],
    }


def create_user(db: sqlite3.Connection, user_data: UserCreate):
    cursor = db.execute(
        "INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)",
        (user_data.username, user_data.email, datetime.now(UTC).isoformat()),
    )
    db.commit()
    row = db.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _row_to_dict(row)


def get_user(db: sqlite3.Connection, user_id: int):
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def get_users(db: sqlite3.Connection):
    rows = db.execute("SELECT * FROM users").fetchall()
    return [_row_to_dict(row) for row in rows]
