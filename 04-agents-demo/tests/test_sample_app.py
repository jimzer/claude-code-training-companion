import sqlite3

import pytest

from sample_app import app


@pytest.fixture
def db(tmp_path):
    """Create a temporary database with the users table."""
    db_path = tmp_path / "app.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
    )
    conn.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("alice", "alice@example.com"),
    )
    conn.commit()
    conn.close()
    # Monkey-patch sqlite3.connect to use our temp db
    original_connect = sqlite3.connect
    sqlite3.connect = lambda _path: original_connect(str(db_path))
    yield db_path
    sqlite3.connect = original_connect


@pytest.fixture
def client(db):
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/process?data=5")
    assert response.status_code == 200
    assert response.json["result"] == 10


def test_get_existing_user(client):
    response = client.get("/users/alice")
    assert response.status_code == 200
    assert response.json["username"] == "alice"
    assert response.json["email"] == "alice@example.com"


def test_get_missing_user(client):
    response = client.get("/users/nobody")
    assert response.status_code == 404


def test_create_user(client):
    response = client.post(
        "/users",
        json={"username": "bob", "email": "bob@example.com"},
    )
    assert response.status_code == 201
    assert response.json["created"] is True


def test_process_missing_data(client):
    """Shows the overly broad except -- returns 500 instead of a helpful error."""
    response = client.get("/process")
    assert response.status_code == 500
    assert response.json["error"] == "Something went wrong"
