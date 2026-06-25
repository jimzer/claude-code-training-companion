"""User model -- maps to the users table in SQLite.

This module exists for reference; the actual table is created in db.py.
Fields:
    id: INTEGER PRIMARY KEY
    username: TEXT UNIQUE NOT NULL
    email: TEXT UNIQUE NOT NULL
    created_at: TEXT (ISO format datetime)
"""
