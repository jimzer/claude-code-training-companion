import pytest
from fastapi.testclient import TestClient

from app.main import app

MISSING_ID = 999


def _create_task(client, **fields):
    payload = {
        "title": "Original",
        "description": "Details",
        "priority": "low",
        **fields,
    }
    response = client.post("/tasks/", json=payload)
    # Not an assert: a setup failure must not count as an expected AssertionError
    # in the xfail tests below.
    response.raise_for_status()
    return response.json()


def _known_defect(reason):
    return pytest.mark.xfail(strict=True, raises=AssertionError, reason=reason)


@pytest.fixture
def no_raise_client(client):
    """Returns the 500 response instead of re-raising the server exception.

    Depends on `client`, which installs the get_db override used by this client.
    """
    return TestClient(app, raise_server_exceptions=False)


# GET /tasks/{task_id}


def test_get_task_returns_created_task(client):
    created = _create_task(client)

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_task_selects_by_id(client):
    first = _create_task(client, title="First")
    second = _create_task(client, title="Second")

    assert client.get(f"/tasks/{first['id']}").json()["title"] == "First"
    assert client.get(f"/tasks/{second['id']}").json()["title"] == "Second"


# PATCH /tasks/{task_id}


def test_patch_updates_only_sent_fields(client):
    created = _create_task(client)

    response = client.patch(f"/tasks/{created['id']}", json={"title": "Renamed"})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Renamed"
    assert data["description"] == "Details"
    assert data["priority"] == "low"
    assert data["completed"] is False
    assert data["id"] == created["id"]
    assert data["created_at"] == created["created_at"]


def test_patch_is_persisted(client):
    created = _create_task(client)

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"title": "Renamed", "priority": "high", "completed": True},
    )

    assert response.status_code == 200
    patched = response.json()
    assert patched["title"] == "Renamed"
    assert patched["priority"] == "high"
    assert patched["completed"] is True
    assert client.get(f"/tasks/{created['id']}").json() == patched


def test_patch_can_reopen_completed_task(client):
    created = _create_task(client)
    completed = client.post(f"/tasks/{created['id']}/complete")
    assert completed.json()["completed"] is True

    response = client.patch(f"/tasks/{created['id']}", json={"completed": False})

    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_patch_explicit_null_clears_description(client):
    created = _create_task(client)

    response = client.patch(f"/tasks/{created['id']}", json={"description": None})

    assert response.status_code == 200
    assert response.json()["description"] is None
    assert response.json()["title"] == "Original"


def test_patch_sets_updated_at(client):
    created = _create_task(client)
    assert created["updated_at"] is None

    response = client.patch(f"/tasks/{created['id']}", json={"title": "Renamed"})

    assert response.status_code == 200
    assert response.json()["updated_at"] is not None


def test_empty_patch_returns_task_unchanged(client):
    created = _create_task(client)

    response = client.patch(f"/tasks/{created['id']}", json={})

    assert response.status_code == 200
    assert response.json() == created
    assert client.get(f"/tasks/{created['id']}").json()["updated_at"] is None


def test_empty_patch_keeps_existing_updated_at(client):
    created = _create_task(client)
    patched = client.patch(f"/tasks/{created['id']}", json={"title": "Renamed"}).json()
    assert patched["updated_at"] is not None

    response = client.patch(f"/tasks/{created['id']}", json={})

    assert response.status_code == 200
    assert response.json() == patched


def test_patch_does_not_touch_other_tasks(client):
    target = _create_task(client, title="Target")
    other = _create_task(client, title="Other")

    response = client.patch(f"/tasks/{target['id']}", json={"title": "Renamed"})

    assert response.json()["title"] == "Renamed"
    assert client.get(f"/tasks/{other['id']}").json() == other


@pytest.mark.parametrize(
    "field",
    [
        pytest.param(
            "title",
            marks=_known_defect(
                "PATCH title=null hits the NOT NULL constraint: IntegrityError, HTTP 500"
            ),
        ),
        pytest.param(
            "priority",
            marks=_known_defect(
                "PATCH priority=null stores NULL, then response validation fails: HTTP 500, "
                "and GET /tasks/ keeps returning 500 afterwards"
            ),
        ),
        pytest.param(
            "completed",
            marks=_known_defect(
                "PATCH completed=null returns 200 and stores NULL: the task leaves both "
                "status filters and the stats counters"
            ),
        ),
    ],
)
def test_patch_null_on_required_field_is_rejected(client, no_raise_client, field):
    created = _create_task(client)

    response = no_raise_client.patch(f"/tasks/{created['id']}", json={field: None})

    assert response.status_code == 422


# DELETE /tasks/{task_id}


def test_delete_returns_204_with_empty_body(client):
    created = _create_task(client)

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_deleted_task_is_gone(client):
    created = _create_task(client)
    assert client.delete(f"/tasks/{created['id']}").status_code == 204

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 404
    assert client.get("/tasks/").json()["pagination"]["total"] == 0


def test_delete_twice_returns_404(client):
    created = _create_task(client)
    assert client.delete(f"/tasks/{created['id']}").status_code == 204

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_keeps_other_tasks(client):
    target = _create_task(client, title="Target")
    other = _create_task(client, title="Other")

    response = client.delete(f"/tasks/{target['id']}")

    assert response.status_code == 204
    assert client.get(f"/tasks/{other['id']}").json() == other


# POST /tasks/{task_id}/complete


def test_complete_marks_task_completed(client):
    created = _create_task(client)
    assert created["completed"] is False

    response = client.post(f"/tasks/{created['id']}/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["updated_at"] is not None
    assert data["title"] == "Original"
    assert data["description"] == "Details"
    assert data["priority"] == "low"
    assert data["created_at"] == created["created_at"]
    assert client.get(f"/tasks/{created['id']}").json() == data


def test_complete_already_completed_task_stays_completed(client):
    created = _create_task(client)
    assert client.post(f"/tasks/{created['id']}/complete").status_code == 200

    response = client.post(f"/tasks/{created['id']}/complete")

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_complete_does_not_touch_other_tasks(client):
    target = _create_task(client, title="Target")
    other = _create_task(client, title="Other")

    response = client.post(f"/tasks/{target['id']}/complete")

    assert response.json()["completed"] is True
    assert client.get(f"/tasks/{other['id']}").json() == other


# 404s


@pytest.mark.parametrize(
    ("method", "path", "body"),
    [
        ("GET", f"/tasks/{MISSING_ID}", None),
        ("PATCH", f"/tasks/{MISSING_ID}", {"title": "Renamed"}),
        ("PATCH", f"/tasks/{MISSING_ID}", {}),
        ("DELETE", f"/tasks/{MISSING_ID}", None),
        ("POST", f"/tasks/{MISSING_ID}/complete", None),
    ],
)
def test_missing_task_returns_404(client, method, path, body):
    response = client.request(method, path, json=body)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
