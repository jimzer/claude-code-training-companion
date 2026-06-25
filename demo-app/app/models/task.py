"""Task model -- maps to the tasks table in SQLite.

This module exists for reference; the actual table is created in db.py.
Fields:
    id: INTEGER PRIMARY KEY
    title: TEXT NOT NULL
    description: TEXT
    completed: INTEGER (0/1)
    priority: TEXT (default 'medium')
    created_at: TEXT (ISO format datetime)
    updated_at: TEXT (ISO format datetime)
    user_id: INTEGER (FK to users.id)
"""
