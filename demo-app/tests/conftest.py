import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.db import get_db
from app.main import app


@pytest.fixture
def db_path(tmp_path):
    """Create a fresh temporary database for each test."""
    path = str(tmp_path / "test.db")
    conn = sqlite3.connect(path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'medium',
            created_at TEXT,
            updated_at TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.close()
    return path


@pytest.fixture
def client(db_path):
    def override_get_db():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
