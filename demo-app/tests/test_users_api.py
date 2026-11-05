import sqlite3
from datetime import UTC, datetime, timedelta

import pytest

ALICE = {"username": "alice", "email": "alice@example.com"}
BOB = {"username": "bob", "email": "bob@example.com"}


def test_create_user_returns_201_and_the_user(client):
    response = client.post("/users/", json=ALICE)

    assert response.status_code == 201
    data = response.json()
    assert set(data) == {"id", "username", "email", "created_at"}
    assert isinstance(data["id"], int)
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"


def test_create_user_assigns_distinct_ids(client):
    first = client.post("/users/", json=ALICE).json()
    second = client.post("/users/", json=BOB).json()

    assert first["id"] != second["id"]


def test_list_users_empty(client):
    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == []


def test_list_users_returns_every_created_user(client):
    alice = client.post("/users/", json=ALICE).json()
    bob = client.post("/users/", json=BOB).json()

    response = client.get("/users/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # get_users has no ORDER BY, so the order is not part of the contract.
    assert alice in data
    assert bob in data


def test_get_user_by_id_returns_the_created_user(client):
    created = client.post("/users/", json=ALICE).json()

    response = client.get(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_user_by_id_selects_the_requested_user(client):
    client.post("/users/", json=ALICE)
    bob = client.post("/users/", json=BOB).json()

    response = client.get(f"/users/{bob['id']}")

    assert response.status_code == 200
    assert response.json()["username"] == "bob"


def test_get_user_not_found(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_with_non_integer_id_returns_422(client):
    response = client.get("/users/not-an-id")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "user_id"]


@pytest.mark.parametrize(
    ("payload", "missing_field"),
    [
        ({"email": "alice@example.com"}, "username"),
        ({"username": "alice"}, "email"),
    ],
)
def test_create_user_missing_required_field_returns_422(client, payload, missing_field):
    response = client.post("/users/", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert [(e["type"], e["loc"]) for e in errors] == [
        ("missing", ["body", missing_field])
    ]


def test_create_user_empty_body_reports_both_fields_as_missing(client):
    response = client.post("/users/", json={})

    assert response.status_code == 422
    locations = {tuple(e["loc"]) for e in response.json()["detail"]}
    assert locations == {("body", "username"), ("body", "email")}


@pytest.mark.parametrize("field", ["username", "email"])
def test_create_user_non_string_field_returns_422(client, field):
    response = client.post("/users/", json={**ALICE, field: 123})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]


def test_rejected_user_is_not_persisted(client):
    client.post("/users/", json={"username": "alice"})

    assert client.get("/users/").json() == []


def test_created_at_is_the_current_utc_time(client):
    before = datetime.now(UTC)
    response = client.post("/users/", json=ALICE)
    after = datetime.now(UTC)

    created_at = datetime.fromisoformat(response.json()["created_at"])
    assert created_at.utcoffset() == timedelta(0)
    # Comparing aware datetimes keeps this independent of the machine's timezone.
    assert before <= created_at <= after


def test_created_at_is_stored_as_utc(client, db_path):
    user = client.post("/users/", json=ALICE).json()

    conn = sqlite3.connect(db_path)
    try:
        stored = conn.execute(
            "SELECT created_at FROM users WHERE id = ?", (user["id"],)
        ).fetchone()[0]
    finally:
        conn.close()

    assert datetime.fromisoformat(stored).utcoffset() == timedelta(0)


def test_created_at_is_stable_across_reads(client):
    created = client.post("/users/", json=ALICE).json()

    fetched = client.get(f"/users/{created['id']}").json()
    listed = client.get("/users/").json()

    assert fetched["created_at"] == created["created_at"]
    assert listed[0]["created_at"] == created["created_at"]
