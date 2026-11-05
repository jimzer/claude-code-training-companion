import sqlite3
from datetime import datetime, timedelta

import pytest

from app.schemas.user import UserCreate
from app.services import user_service


@pytest.fixture
def db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    yield conn
    conn.close()


def _add_user(db, username="alice", email="alice@example.com"):
    return user_service.create_user(db, UserCreate(username=username, email=email))


def _committed_usernames(db_path):
    """Read through a second connection, which only sees committed data."""
    conn = sqlite3.connect(db_path)
    try:
        return [row[0] for row in conn.execute("SELECT username FROM users")]
    finally:
        conn.close()


def test_create_user_returns_all_fields(db):
    user = _add_user(db, username="bob", email="bob@example.com")

    assert user["id"] >= 1
    assert user["username"] == "bob"
    assert user["email"] == "bob@example.com"
    assert user["created_at"] is not None


def test_create_user_created_at_is_utc(db):
    user = _add_user(db)

    assert datetime.fromisoformat(user["created_at"]).utcoffset() == timedelta(0)


def test_create_user_commits(db, db_path):
    _add_user(db, username="alice")

    assert _committed_usernames(db_path) == ["alice"]


@pytest.mark.parametrize(
    ("username", "email"),
    [
        ("alice", "other@example.com"),
        ("other", "alice@example.com"),
    ],
    ids=["duplicate_username", "duplicate_email"],
)
def test_create_user_duplicate_raises_and_adds_nothing(db, db_path, username, email):
    _add_user(db, username="alice", email="alice@example.com")

    with pytest.raises(sqlite3.IntegrityError):
        _add_user(db, username=username, email=email)

    assert _committed_usernames(db_path) == ["alice"]


def test_get_user_returns_created_user(db):
    user = _add_user(db)

    assert user_service.get_user(db, user["id"]) == user


def test_get_user_missing_returns_none(db):
    assert user_service.get_user(db, 999) is None


def test_get_users_empty(db):
    assert user_service.get_users(db) == []


def test_get_users_returns_every_user(db):
    alice = _add_user(db, username="alice", email="alice@example.com")
    bob = _add_user(db, username="bob", email="bob@example.com")

    users = {user["id"]: user for user in user_service.get_users(db)}

    assert users == {alice["id"]: alice, bob["id"]: bob}
