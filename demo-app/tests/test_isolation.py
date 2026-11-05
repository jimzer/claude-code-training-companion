"""The test fixtures must never touch the database at the default path.

The app lifespan runs init_db(), which drops every table. Each test here works
in a temporary cwd and sets app.db.DB_PATH to the default relative path, so a
broken fixture only damages a throwaway file, even if DATABASE_PATH is set.

`client` is requested through getfixturevalue so that its lifespan is guaranteed
to run after the setup below, and so that its own DB_PATH patch wins.
"""

import sqlite3
from contextlib import closing

import pytest

from app.config import Settings

DEFAULT_DB = Settings.model_fields["database_path"].default


def read_titles(path):
    with closing(sqlite3.connect(path)) as conn:
        return [row[0] for row in conn.execute("SELECT title FROM tasks ORDER BY id")]


@pytest.fixture
def default_path(tmp_path, monkeypatch):
    """Make the default relative database path resolve inside a temporary cwd."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    monkeypatch.setattr("app.db.DB_PATH", DEFAULT_DB)
    return cwd / DEFAULT_DB


@pytest.fixture
def existing_db(default_path):
    """Put a database holding one task at the default path."""
    with closing(sqlite3.connect(default_path)) as conn:
        conn.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT)")
        conn.execute("INSERT INTO tasks (title) VALUES ('precious')")
        conn.commit()
    return default_path


def test_client_keeps_existing_default_db_data(existing_db, request):
    client = request.getfixturevalue("client")

    assert client.post("/tasks/", json={"title": "from test"}).status_code == 201

    assert read_titles(existing_db) == ["precious"]


def test_client_does_not_create_default_db(default_path, request):
    client = request.getfixturevalue("client")

    assert client.post("/tasks/", json={"title": "from test"}).status_code == 201

    assert not default_path.exists()


def test_client_writes_to_temp_db(default_path, request):
    client = request.getfixturevalue("client")

    assert client.post("/tasks/", json={"title": "from test"}).status_code == 201

    assert read_titles(request.getfixturevalue("db_path")) == ["from test"]
