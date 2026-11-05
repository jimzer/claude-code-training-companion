"""Request validation on the /tasks routes: bodies, path ids, query bounds, defaults."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

SQLITE_MAX_INTEGER = 2**63 - 1

ID_ROUTES = [
    ("GET", "/tasks/{}"),
    ("PATCH", "/tasks/{}"),
    ("DELETE", "/tasks/{}"),
    ("POST", "/tasks/{}/complete"),
]


@pytest.fixture
def client_no_raise(client):
    """Report server exceptions as a 500 instead of re-raising them in the test."""
    return TestClient(app, raise_server_exceptions=False)


def error_locations(response):
    return [tuple(error["loc"]) for error in response.json()["detail"]]


def task_count(client):
    return client.get("/tasks/").json()["stats"]["total"]


# --- POST /tasks/: invalid bodies ---


@pytest.mark.parametrize(
    ("body", "location"),
    [
        ({}, ("body", "title")),
        ({"description": "No title"}, ("body", "title")),
        ({"title": None}, ("body", "title")),
        ({"title": 123}, ("body", "title")),
        ({"title": ["a"]}, ("body", "title")),
        ({"title": "T", "description": 123}, ("body", "description")),
        ({"title": "T", "priority": None}, ("body", "priority")),
        ({"title": "T", "priority": 1}, ("body", "priority")),
        ({"title": "T", "user_id": "abc"}, ("body", "user_id")),
        (["not", "an", "object"], ("body",)),
    ],
)
def test_create_task_invalid_body_returns_422(client, body, location):
    response = client.post("/tasks/", json=body)

    assert response.status_code == 422
    assert location in error_locations(response)
    assert task_count(client) == 0


def test_create_task_without_body_returns_422(client):
    response = client.post("/tasks/")

    assert response.status_code == 422
    assert ("body",) in error_locations(response)


@pytest.mark.parametrize(
    ("content", "content_type"),
    [
        ('{"title": ', "application/json"),
        ("title=T", "text/plain"),
    ],
)
def test_create_task_unparseable_body_returns_422(client, content, content_type):
    response = client.post(
        "/tasks/", content=content, headers={"content-type": content_type}
    )

    assert response.status_code == 422
    assert task_count(client) == 0


# --- POST /tasks/: defaults and unknown fields ---


def test_create_task_applies_defaults(client):
    response = client.post("/tasks/", json={"title": "Only a title"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Only a title"
    assert data["description"] is None
    assert data["priority"] == "medium"
    assert data["completed"] is False
    assert data["user_id"] is None
    assert data["updated_at"] is None


def test_create_task_ignores_unknown_fields(client):
    response = client.post("/tasks/", json={"title": "T", "unknown": "ignored"})

    assert response.status_code == 201
    assert "unknown" not in response.json()


def test_create_task_ignores_server_managed_fields(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "T",
            "id": 999,
            "completed": True,
            "created_at": "2000-01-01T00:00:00Z",
            "updated_at": "2000-01-01T00:00:00Z",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] != 999
    assert data["completed"] is False
    assert not data["created_at"].startswith("2000")
    assert data["updated_at"] is None
    assert client.get("/tasks/999").status_code == 404


# --- PATCH /tasks/{id}: invalid bodies ---


@pytest.mark.parametrize(
    ("body", "location"),
    [
        ({"title": 123}, ("body", "title")),
        ({"description": 123}, ("body", "description")),
        ({"priority": 1}, ("body", "priority")),
        ({"completed": "not-a-boolean"}, ("body", "completed")),
        ({"user_id": "abc"}, ("body", "user_id")),
        (["not", "an", "object"], ("body",)),
    ],
)
def test_update_task_invalid_body_returns_422(client, body, location):
    created = client.post("/tasks/", json={"title": "Original"}).json()

    response = client.patch(f"/tasks/{created['id']}", json=body)

    assert response.status_code == 422
    assert location in error_locations(response)
    assert client.get(f"/tasks/{created['id']}").json() == created


def test_update_task_without_body_returns_422(client):
    created = client.post("/tasks/", json={"title": "Original"}).json()

    response = client.patch(f"/tasks/{created['id']}")

    assert response.status_code == 422
    assert ("body",) in error_locations(response)


def test_update_task_validates_body_before_looking_up_the_task(client):
    response = client.patch("/tasks/999", json={"title": 123})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field",
    [
        pytest.param(
            "title",
            marks=pytest.mark.xfail(
                strict=True,
                raises=AssertionError,
                reason="TaskUpdate accepts title=null, which violates NOT NULL: "
                "sqlite3.IntegrityError, so a 500",
            ),
        ),
        pytest.param(
            "priority",
            marks=pytest.mark.xfail(
                strict=True,
                raises=AssertionError,
                reason="TaskUpdate accepts priority=null and stores it: TaskResponse "
                "then fails to serialize the task, so a 500",
            ),
        ),
        pytest.param(
            "completed",
            marks=pytest.mark.xfail(
                strict=True,
                raises=AssertionError,
                reason="TaskUpdate accepts completed=null and stores it: 200, and the "
                "task then counts as neither pending nor completed in the stats",
            ),
        ),
    ],
)
def test_update_task_null_on_non_nullable_field_returns_422(client_no_raise, field):
    created = client_no_raise.post("/tasks/", json={"title": "Original"}).json()

    response = client_no_raise.patch(f"/tasks/{created['id']}", json={field: None})

    assert response.status_code == 422


def test_update_task_null_clears_nullable_fields(client):
    user = client.post(
        "/users/", json={"username": "alice", "email": "alice@example.com"}
    ).json()
    created = client.post(
        "/tasks/",
        json={"title": "Original", "description": "Text", "user_id": user["id"]},
    ).json()

    response = client.patch(
        f"/tasks/{created['id']}", json={"description": None, "user_id": None}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["description"] is None
    assert data["user_id"] is None
    assert data["title"] == "Original"


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="A user_id that matches no user passes validation, then violates the "
    "foreign key: sqlite3.IntegrityError, so a 500",
)
@pytest.mark.parametrize("method", ["POST", "PATCH"])
def test_user_id_without_user_is_a_client_error(client_no_raise, method):
    created = client_no_raise.post("/tasks/", json={"title": "Original"}).json()
    path = "/tasks/" if method == "POST" else f"/tasks/{created['id']}"

    response = client_no_raise.request(
        method, path, json={"title": "T", "user_id": 999}
    )

    assert 400 <= response.status_code < 500


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="A user_id above the SQLite INTEGER range passes validation, then raises "
    "OverflowError when bound to the query, so a 500",
)
@pytest.mark.parametrize("method", ["POST", "PATCH"])
def test_user_id_above_sqlite_range_is_a_client_error(client_no_raise, method):
    created = client_no_raise.post("/tasks/", json={"title": "Original"}).json()
    path = "/tasks/" if method == "POST" else f"/tasks/{created['id']}"

    response = client_no_raise.request(
        method, path, json={"title": "T", "user_id": SQLITE_MAX_INTEGER + 1}
    )

    assert 400 <= response.status_code < 500


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="A title with a lone surrogate is valid JSON and passes validation, then "
    "raises UnicodeEncodeError when bound to the query, so a 500",
)
def test_create_task_title_with_lone_surrogate_is_a_client_error(client_no_raise):
    response = client_no_raise.post(
        "/tasks/",
        content=b'{"title": "\\ud800"}',
        headers={"content-type": "application/json"},
    )

    assert 400 <= response.status_code < 500


# --- PATCH /tasks/{id}: unknown fields ---


def test_update_task_with_only_unknown_fields_changes_nothing(client):
    created = client.post("/tasks/", json={"title": "Original"}).json()

    response = client.patch(f"/tasks/{created['id']}", json={"unknown": "ignored"})

    assert response.status_code == 200
    assert response.json() == created
    assert client.get(f"/tasks/{created['id']}").json() == created


def test_update_task_ignores_unknown_and_server_managed_fields(client):
    created = client.post("/tasks/", json={"title": "Original"}).json()

    response = client.patch(
        f"/tasks/{created['id']}",
        json={
            "title": "Renamed",
            "unknown": "ignored",
            "id": 999,
            "created_at": "2000-01-01T00:00:00Z",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Renamed"
    assert data["id"] == created["id"]
    assert data["created_at"] == created["created_at"]
    assert "unknown" not in data


# --- Path id ---


@pytest.mark.parametrize(("method", "path"), ID_ROUTES)
@pytest.mark.parametrize("task_id", ["abc", "1.5"])
def test_non_integer_task_id_returns_422(client, method, path, task_id):
    response = client.request(method, path.format(task_id), json={})

    assert response.status_code == 422
    assert ("path", "task_id") in error_locations(response)


@pytest.mark.parametrize(("method", "path"), ID_ROUTES)
@pytest.mark.parametrize("task_id", [0, -1, SQLITE_MAX_INTEGER])
def test_integer_task_id_without_task_returns_404(client, method, path, task_id):
    response = client.request(method, path.format(task_id), json={})

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="An id above the SQLite INTEGER range passes validation, then raises "
    "OverflowError when bound to the query, so a 500",
)
@pytest.mark.parametrize(("method", "path"), ID_ROUTES)
def test_task_id_above_sqlite_range_is_a_client_error(client_no_raise, method, path):
    response = client_no_raise.request(
        method, path.format(SQLITE_MAX_INTEGER + 1), json={}
    )

    assert response.status_code in (404, 422)


# --- GET /tasks/: query bounds ---


@pytest.mark.parametrize("value", ["0", "-1", "abc", "1.5"])
def test_invalid_page_returns_422(client, value):
    response = client.get("/tasks/", params={"page": value})

    assert response.status_code == 422
    assert ("query", "page") in error_locations(response)


@pytest.mark.parametrize("value", ["0", "-1", "101", "abc", "1.5"])
def test_invalid_page_size_returns_422(client, value):
    response = client.get("/tasks/", params={"page_size": value})

    assert response.status_code == 422
    assert ("query", "page_size") in error_locations(response)


def test_page_lower_bound_is_accepted(client):
    response = client.get("/tasks/", params={"page": 1})

    assert response.status_code == 200
    assert response.json()["pagination"]["page"] == 1


def test_very_large_page_is_clamped(client):
    client.post("/tasks/", json={"title": "Only task"})

    response = client.get("/tasks/", params={"page": 2**64})

    assert response.status_code == 200
    assert response.json()["pagination"]["page"] == 1
    assert len(response.json()["items"]) == 1


def test_page_size_lower_bound_is_accepted(client):
    for i in range(2):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/", params={"page_size": 1})

    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["page_size"] == 1
    assert len(data["items"]) == 1
    assert data["pagination"]["total_pages"] == 2


def test_page_size_upper_bound_is_accepted(client):
    for i in range(101):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/", params={"page_size": 100})

    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["page_size"] == 100
    assert len(data["items"]) == 100
    assert data["pagination"]["has_next"] is True


def test_default_page_size_limits_items_to_20(client):
    for i in range(21):
        client.post("/tasks/", json={"title": f"Task {i}"})

    data = client.get("/tasks/").json()

    assert len(data["items"]) == 20
    assert data["pagination"]["page_size"] == 20
    assert data["pagination"]["total"] == 21
    assert data["pagination"]["total_pages"] == 2


def test_unknown_query_parameter_is_ignored(client):
    client.post("/tasks/", json={"title": "Task"})

    response = client.get("/tasks/", params={"unknown": "ignored"})

    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
