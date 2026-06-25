def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={"title": "Test task", "description": "A test task", "priority": "high"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["priority"] == "high"
    assert data["completed"] is False


def test_get_tasks(client):
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["pagination"]["total"] == 2
    assert data["pagination"]["page"] == 1
    assert data["stats"]["total"] == 2


def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_pagination_defaults(client):
    response = client.get("/tasks/")
    data = response.json()
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 20
    assert data["pagination"]["total"] == 0
    assert data["pagination"]["total_pages"] == 1
    assert data["pagination"]["has_next"] is False
    assert data["pagination"]["has_previous"] is False
    assert data["items"] == []
    assert data["stats"]["total"] == 0
    assert data["stats"]["pending"] == 0
    assert data["stats"]["completed"] == 0


def test_pagination_page_size(client):
    for i in range(5):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/?page_size=2")
    data = response.json()
    assert len(data["items"]) == 2
    assert data["pagination"]["total"] == 5
    assert data["pagination"]["total_pages"] == 3
    assert data["pagination"]["has_next"] is True
    assert data["pagination"]["has_previous"] is False


def test_pagination_second_page(client):
    for i in range(5):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/?page=2&page_size=2")
    data = response.json()
    assert len(data["items"]) == 2
    assert data["pagination"]["page"] == 2
    assert data["pagination"]["has_next"] is True
    assert data["pagination"]["has_previous"] is True


def test_pagination_last_page(client):
    for i in range(5):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/?page=3&page_size=2")
    data = response.json()
    assert len(data["items"]) == 1
    assert data["pagination"]["page"] == 3
    assert data["pagination"]["has_next"] is False
    assert data["pagination"]["has_previous"] is True


def test_pagination_beyond_last_page_clamps(client):
    for i in range(3):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/?page=999&page_size=2")
    data = response.json()
    assert data["pagination"]["page"] == 2  # clamped to last page
    assert len(data["items"]) == 1


def test_filter_by_status(client):
    client.post("/tasks/", json={"title": "Task 1"})
    resp = client.post("/tasks/", json={"title": "Task 2"})
    task_id = resp.json()["id"]
    client.post(f"/tasks/{task_id}/complete")

    response = client.get("/tasks/?status=pending")
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["completed"] is False
    assert data["pagination"]["total"] == 1
    # Stats remain global
    assert data["stats"]["total"] == 2
    assert data["stats"]["pending"] == 1
    assert data["stats"]["completed"] == 1


def test_filter_by_priority(client):
    client.post("/tasks/", json={"title": "High", "priority": "high"})
    client.post("/tasks/", json={"title": "Low", "priority": "low"})

    response = client.get("/tasks/?priority=high")
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["priority"] == "high"
    assert data["pagination"]["total"] == 1
    assert data["stats"]["total"] == 2


def test_filter_combined(client):
    client.post("/tasks/", json={"title": "High pending", "priority": "high"})
    resp = client.post("/tasks/", json={"title": "High done", "priority": "high"})
    client.post(f"/tasks/{resp.json()['id']}/complete")
    client.post("/tasks/", json={"title": "Low pending", "priority": "low"})

    response = client.get("/tasks/?status=pending&priority=high")
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "High pending"
    assert data["stats"]["total"] == 3


def test_invalid_filter_returns_422(client):
    response = client.get("/tasks/?status=invalid")
    assert response.status_code == 422

    response = client.get("/tasks/?priority=invalid")
    assert response.status_code == 422


def test_ordering_desc(client):
    client.post("/tasks/", json={"title": "First"})
    client.post("/tasks/", json={"title": "Second"})

    response = client.get("/tasks/")
    data = response.json()
    assert data["items"][0]["title"] == "Second"
    assert data["items"][1]["title"] == "First"
