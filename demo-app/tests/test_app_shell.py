"""Application shell: root redirect, static files, trailing-slash redirects."""

import pytest


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_leads_to_the_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert str(response.url) == "http://testserver/static/index.html"


def test_static_index_is_served_as_html(client):
    response = client.get("/static/index.html", follow_redirects=False)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<title>Task Manager</title>" in response.text


def test_missing_static_file_returns_404(client):
    response = client.get("/static/missing.html", follow_redirects=False)
    assert response.status_code == 404


@pytest.mark.parametrize(
    ("path", "location"),
    [
        ("/tasks", "http://testserver/tasks/"),
        ("/users", "http://testserver/users/"),
        ("/tasks?page=2&page_size=5", "http://testserver/tasks/?page=2&page_size=5"),
        ("/tasks/1/", "http://testserver/tasks/1"),
        ("/users/1/", "http://testserver/users/1"),
    ],
)
def test_get_redirects_to_the_canonical_path(client, path, location):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == location


def test_following_the_tasks_redirect_reaches_the_list(client):
    client.post("/tasks/", json={"title": "Task 1"})

    response = client.get("/tasks?page_size=5")
    assert response.status_code == 200
    assert str(response.url) == "http://testserver/tasks/?page_size=5"
    data = response.json()
    assert [item["title"] for item in data["items"]] == ["Task 1"]
    assert data["pagination"]["page_size"] == 5


def test_following_the_users_redirect_reaches_the_list(client):
    client.post("/users/", json={"username": "alice", "email": "alice@example.com"})

    response = client.get("/users")
    assert response.status_code == 200
    assert str(response.url) == "http://testserver/users/"
    assert [user["username"] for user in response.json()] == ["alice"]


def test_unfollowed_post_redirect_creates_nothing(client):
    response = client.post(
        "/tasks", json={"title": "Not created"}, follow_redirects=False
    )
    assert response.status_code == 307
    assert response.headers["location"] == "http://testserver/tasks/"
    assert client.get("/tasks/").json()["pagination"]["total"] == 0


def test_followed_post_redirect_keeps_method_and_body(client):
    response = client.post("/tasks", json={"title": "Created"})
    assert response.status_code == 201
    assert response.json()["title"] == "Created"
    assert client.get("/tasks/").json()["pagination"]["total"] == 1


@pytest.mark.parametrize("path", ["/unknown", "/unknown/"])
def test_unknown_route_returns_404_without_redirect(client, path):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 404
    assert "location" not in response.headers
