import pytest
from fastapi.testclient import TestClient

from app.db import init_db
from app.main import app


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    """Create a fresh temporary database for each test and point the app at it.

    Patching app.db.DB_PATH covers both get_db and the app lifespan, which runs
    init_db() and so drops every table in the database it is pointed at.
    """
    path = str(tmp_path / "test.db")
    monkeypatch.setattr("app.db.DB_PATH", path)
    init_db()
    return path


@pytest.fixture
def client(db_path):
    with TestClient(app) as c:
        yield c
