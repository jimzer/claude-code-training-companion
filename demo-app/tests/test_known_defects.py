"""Known defects of the demo app, written as the behaviour we expect.

Each test fails today. A strict xfail makes the suite fail as soon as the app
meets the expected behaviour, which forces the marker to be removed.

`raises=AssertionError` stops a broken setup from counting as an xfail: setup
goes through the raising `client` and `raise_for_status()`, so it raises something
else and is reported as a real failure, even from a fixture.

Limit: `non_raising_client` turns every server exception into a 500, so these
tests cannot tell the defect in their reason from an unrelated crash on the same
route. The causes were checked by hand with the raising client.
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def non_raising_client(client):
    """Report server exceptions as HTTP 500 instead of re-raising them."""
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def task_id(client):
    response = client.post("/tasks/", json={"title": "Existing task"})
    response.raise_for_status()
    return response.json()["id"]


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="update_task stamps updated_at with a naive datetime.now(), "
    "intentional training defect",
)
def test_updated_at_is_utc_after_patch(client, task_id):
    response = client.patch(f"/tasks/{task_id}", json={"title": "New"})

    updated_at = datetime.fromisoformat(response.json()["updated_at"])
    assert updated_at.tzinfo is not None
    assert updated_at.utcoffset() == timedelta(0)


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="sqlite3.IntegrityError (FOREIGN KEY) is not handled by create_task",
)
def test_create_task_with_unknown_user_is_client_error(non_raising_client):
    response = non_raising_client.post(
        "/tasks/", json={"title": "Orphan task", "user_id": 999}
    )
    assert 400 <= response.status_code < 500


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="sqlite3.IntegrityError (UNIQUE) is not handled by create_user",
)
def test_create_duplicate_user_is_client_error(client, non_raising_client):
    user = {"username": "alice", "email": "alice@example.com"}
    client.post("/users/", json=user).raise_for_status()

    response = non_raising_client.post("/users/", json=user)
    assert 400 <= response.status_code < 500


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="TaskUpdate accepts title=None, then sqlite3.IntegrityError (NOT NULL) "
    "is not handled by update_task",
)
def test_patch_null_title_is_client_error(non_raising_client, task_id):
    response = non_raising_client.patch(f"/tasks/{task_id}", json={"title": None})
    assert 400 <= response.status_code < 500


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="TaskUpdate accepts priority=None and stores it, then TaskResponse "
    "rejects it with a ResponseValidationError",
)
def test_patch_null_priority_is_client_error(non_raising_client, task_id):
    response = non_raising_client.patch(f"/tasks/{task_id}", json={"priority": None})
    assert 400 <= response.status_code < 500


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="PATCH priority=null commits the NULL before its own 500, then every "
    "GET /tasks/ page holding that row fails with a ResponseValidationError",
)
def test_list_tasks_still_works_after_patch_null_priority(non_raising_client, task_id):
    # The status of this PATCH is covered by the test above.
    non_raising_client.patch(f"/tasks/{task_id}", json={"priority": None})

    response = non_raising_client.get("/tasks/")
    assert response.status_code == 200
    assert response.json()["items"][0]["priority"] in {"low", "medium", "high"}


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="TaskBase.priority is a free-form str, so POST /tasks/ stores any value "
    "and answers 201",
)
def test_create_task_with_unknown_priority_is_rejected(client):
    response = client.post("/tasks/", json={"title": "Task", "priority": "urgent"})
    assert response.status_code == 422
