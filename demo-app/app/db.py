import sqlite3
from pathlib import Path

from app.config import get_settings

settings = get_settings()

DB_PATH = settings.database_path


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = get_connection()
    conn.executescript("""
        DROP TABLE IF EXISTS tasks;
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT
        );
        CREATE TABLE tasks (
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
