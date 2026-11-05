import sqlite3
from datetime import datetime, timedelta

import pytest

from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.user import UserCreate
from app.services import task_service, user_service


@pytest.fixture
def db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    yield conn
    conn.close()


def _add_task(db, title="Task", **fields):
    return task_service.create_task(db, TaskCreate(title=title, **fields))


def _add_dated_tasks(db, seconds):
    """Create one task per value, dated so that sort order is unambiguous.

    Tasks created back to back can share a `created_at`, and the sort has no
    tiebreaker, so any test relying on order must set distinct timestamps.
    """
    for second in seconds:
        task = _add_task(db, title=f"Task {second}")
        db.execute(
            "UPDATE tasks SET created_at = ? WHERE id = ?",
            (f"2026-01-01T00:00:{second:02d}+00:00", task["id"]),
        )
    db.commit()


def _add_user(db):
    return user_service.create_user(
        db, UserCreate(username="alice", email="alice@example.com")
    )


def _committed_row(db_path, task_id):
    """Read through a second connection, which only sees committed data."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    finally:
        conn.close()


def _titles(result):
    return [item["title"] for item in result["items"]]


# create_task


def test_create_task_returns_all_fields(db):
    task = _add_task(db, title="Write", description="Some tests", priority="high")

    assert task["id"] >= 1
    assert task["title"] == "Write"
    assert task["description"] == "Some tests"
    assert task["priority"] == "high"
    assert task["completed"] is False
    assert task["updated_at"] is None
    assert task["user_id"] is None


def test_create_task_applies_defaults(db):
    task = _add_task(db, title="Minimal")

    assert task["description"] is None
    assert task["priority"] == "medium"


def test_create_task_created_at_is_utc(db):
    task = _add_task(db)

    assert datetime.fromisoformat(task["created_at"]).utcoffset() == timedelta(0)


def test_create_task_commits(db, db_path):
    task = _add_task(db, title="Saved")

    assert _committed_row(db_path, task["id"])["title"] == "Saved"


def test_create_task_with_existing_user(db):
    user = _add_user(db)

    task = _add_task(db, user_id=user["id"])

    assert task["user_id"] == user["id"]


def test_create_task_with_unknown_user_violates_foreign_key(db, db_path):
    with pytest.raises(sqlite3.IntegrityError):
        _add_task(db, user_id=999)

    assert _committed_row(db_path, 1) is None


# get_task


def test_get_task_returns_created_task(db):
    task = _add_task(db, title="Find me")

    assert task_service.get_task(db, task["id"]) == task


def test_get_task_missing_returns_none(db):
    assert task_service.get_task(db, 999) is None


# get_tasks


def test_get_tasks_empty(db):
    assert task_service.get_tasks(db) == []


def test_get_tasks_returns_every_task(db):
    first = _add_task(db, title="First")
    second = _add_task(db, title="Second")
    task_service.complete_task(db, second["id"])

    tasks = {task["id"]: task for task in task_service.get_tasks(db)}

    assert set(tasks) == {first["id"], second["id"]}
    assert tasks[first["id"]]["completed"] is False
    assert tasks[second["id"]]["completed"] is True


# update_task


def test_update_task_changes_only_given_fields(db):
    user = _add_user(db)
    task = _add_task(
        db, title="Old", description="Kept", priority="low", user_id=user["id"]
    )

    updated = task_service.update_task(db, task["id"], TaskUpdate(title="New"))

    assert updated["title"] == "New"
    assert updated["description"] == "Kept"
    assert updated["priority"] == "low"
    assert updated["completed"] is False
    assert updated["user_id"] == user["id"]
    assert updated["created_at"] == task["created_at"]
    assert updated["updated_at"] is not None


def test_update_task_leaves_other_tasks_alone(db):
    target = _add_task(db, title="Target")
    other = _add_task(db, title="Other")

    task_service.update_task(db, target["id"], TaskUpdate(title="Changed"))

    assert task_service.get_task(db, other["id"]) == other


def test_update_task_commits(db, db_path):
    task = _add_task(db, title="Old")

    task_service.update_task(db, task["id"], TaskUpdate(title="New"))

    assert _committed_row(db_path, task["id"])["title"] == "New"


def test_update_task_can_clear_description(db):
    task = _add_task(db, description="To remove")

    updated = task_service.update_task(db, task["id"], TaskUpdate(description=None))

    assert updated["description"] is None


@pytest.mark.parametrize("completed", [True, False])
def test_update_task_sets_completed_as_bool(db, completed):
    task = _add_task(db)
    if not completed:
        task_service.complete_task(db, task["id"])

    updated = task_service.update_task(db, task["id"], TaskUpdate(completed=completed))

    assert updated["completed"] is completed


def test_update_task_assigns_and_clears_user(db):
    user = _add_user(db)
    task = _add_task(db)

    assigned = task_service.update_task(db, task["id"], TaskUpdate(user_id=user["id"]))
    cleared = task_service.update_task(db, task["id"], TaskUpdate(user_id=None))

    assert assigned["user_id"] == user["id"]
    assert cleared["user_id"] is None


@pytest.mark.xfail(
    strict=True,
    reason=(
        "TaskUpdate accepts an explicit null and update_task writes it: "
        "IntegrityError on title, NULL stored in priority and completed"
    ),
)
@pytest.mark.parametrize("field", ["title", "priority", "completed"])
def test_update_task_explicit_null_keeps_required_field(db, field):
    task = _add_task(db)
    task = task_service.complete_task(db, task["id"])

    updated = task_service.update_task(db, task["id"], TaskUpdate(**{field: None}))

    assert updated[field] == task[field]


def test_update_task_without_fields_returns_task_unchanged(db):
    task = _add_task(db)

    assert task_service.update_task(db, task["id"], TaskUpdate()) == task
    assert task_service.get_task(db, task["id"]) == task


def test_update_task_missing_returns_none(db):
    assert task_service.update_task(db, 999, TaskUpdate(title="New")) is None
    assert task_service.get_tasks(db) == []


def test_update_task_with_unknown_user_violates_foreign_key(db, db_path):
    task = _add_task(db)

    with pytest.raises(sqlite3.IntegrityError):
        task_service.update_task(db, task["id"], TaskUpdate(user_id=999))

    assert _committed_row(db_path, task["id"])["user_id"] is None


# delete_task


def test_delete_task_removes_only_that_task(db):
    target = _add_task(db, title="Target")
    other = _add_task(db, title="Other")

    assert task_service.delete_task(db, target["id"]) is True

    assert task_service.get_task(db, target["id"]) is None
    assert task_service.get_task(db, other["id"]) == other


def test_delete_task_commits(db, db_path):
    task = _add_task(db)

    task_service.delete_task(db, task["id"])

    assert _committed_row(db_path, task["id"]) is None


def test_delete_task_missing_returns_false(db):
    assert task_service.delete_task(db, 999) is False


def test_delete_task_twice_returns_false(db):
    task = _add_task(db)

    task_service.delete_task(db, task["id"])

    assert task_service.delete_task(db, task["id"]) is False


# complete_task


def test_complete_task_marks_completed_and_keeps_other_fields(db):
    user = _add_user(db)
    task = _add_task(
        db, title="Do", description="Now", priority="high", user_id=user["id"]
    )

    completed = task_service.complete_task(db, task["id"])

    assert completed["completed"] is True
    assert completed["title"] == "Do"
    assert completed["description"] == "Now"
    assert completed["priority"] == "high"
    assert completed["user_id"] == user["id"]
    assert completed["created_at"] == task["created_at"]


def test_complete_task_updated_at_is_utc(db):
    task = _add_task(db)

    completed = task_service.complete_task(db, task["id"])

    assert datetime.fromisoformat(completed["updated_at"]).utcoffset() == timedelta(0)


def test_complete_task_commits(db, db_path):
    task = _add_task(db)

    task_service.complete_task(db, task["id"])

    assert _committed_row(db_path, task["id"])["completed"] == 1


def test_complete_task_twice_stays_completed(db):
    task = _add_task(db)

    task_service.complete_task(db, task["id"])

    assert task_service.complete_task(db, task["id"])["completed"] is True


def test_complete_task_missing_returns_none(db):
    assert task_service.complete_task(db, 999) is None


# get_tasks_paginated: pagination


def test_paginated_empty_table(db):
    assert task_service.get_tasks_paginated(db) == {
        "items": [],
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total": 0,
            "total_pages": 1,
            "has_next": False,
            "has_previous": False,
        },
        "stats": {"total": 0, "pending": 0, "completed": 0},
    }


@pytest.mark.parametrize(
    ("task_count", "page_size", "total_pages"),
    [
        (0, 2, 1),
        (1, 2, 1),
        (2, 2, 1),
        (3, 2, 2),
        (4, 2, 2),
        (5, 2, 3),
    ],
)
def test_paginated_total_pages(db, task_count, page_size, total_pages):
    for _ in range(task_count):
        _add_task(db)

    result = task_service.get_tasks_paginated(db, page_size=page_size)

    assert result["pagination"]["total"] == task_count
    assert result["pagination"]["total_pages"] == total_pages


def test_paginated_sorts_by_created_at_descending(db):
    # Insertion order differs from date order, so only the sort can pass this.
    _add_dated_tasks(db, [2, 0, 3, 1])

    result = task_service.get_tasks_paginated(db)

    assert _titles(result) == ["Task 3", "Task 2", "Task 1", "Task 0"]


def test_paginated_walks_through_pages(db):
    _add_dated_tasks(db, [0, 1, 2, 3, 4])

    pages = [
        task_service.get_tasks_paginated(db, page=page, page_size=2)
        for page in (1, 2, 3)
    ]

    assert [_titles(page) for page in pages] == [
        ["Task 4", "Task 3"],
        ["Task 2", "Task 1"],
        ["Task 0"],
    ]
    assert [page["pagination"]["has_next"] for page in pages] == [True, True, False]
    assert [page["pagination"]["has_previous"] for page in pages] == [
        False,
        True,
        True,
    ]


def test_paginated_clamps_page_beyond_last(db):
    _add_dated_tasks(db, [0, 1, 2])

    result = task_service.get_tasks_paginated(db, page=999, page_size=2)

    assert result["pagination"]["page"] == 2
    assert result["pagination"]["has_next"] is False
    assert result["pagination"]["has_previous"] is True
    assert _titles(result) == ["Task 0"]


def test_paginated_clamps_page_to_one_on_empty_table(db):
    result = task_service.get_tasks_paginated(db, page=999)

    assert result["pagination"]["page"] == 1
    assert result["pagination"]["has_previous"] is False
    assert result["items"] == []


def test_paginated_clamps_against_filtered_total(db):
    for _ in range(4):
        _add_task(db, priority="low")
    _add_task(db, title="Only high", priority="high")

    result = task_service.get_tasks_paginated(db, page=3, page_size=1, priority="high")

    assert result["pagination"]["page"] == 1
    assert result["pagination"]["total_pages"] == 1
    assert _titles(result) == ["Only high"]


# get_tasks_paginated: filters and stats


@pytest.fixture
def mixed_tasks(db):
    """Three pending and two completed tasks, across two priorities."""
    _add_task(db, title="Pending low", priority="low")
    _add_task(db, title="Pending high 1", priority="high")
    _add_task(db, title="Pending high 2", priority="high")
    done_low = _add_task(db, title="Done low", priority="low")
    done_high = _add_task(db, title="Done high", priority="high")
    task_service.complete_task(db, done_low["id"])
    task_service.complete_task(db, done_high["id"])


@pytest.mark.parametrize(
    ("filters", "expected_titles"),
    [
        (
            {},
            {
                "Pending low",
                "Pending high 1",
                "Pending high 2",
                "Done low",
                "Done high",
            },
        ),
        ({"status": "pending"}, {"Pending low", "Pending high 1", "Pending high 2"}),
        ({"status": "completed"}, {"Done low", "Done high"}),
        ({"priority": "low"}, {"Pending low", "Done low"}),
        ({"status": "completed", "priority": "high"}, {"Done high"}),
        ({"priority": "medium"}, set()),
    ],
)
def test_paginated_filters_items_but_keeps_stats_global(
    db, mixed_tasks, filters, expected_titles
):
    result = task_service.get_tasks_paginated(db, **filters)

    assert set(_titles(result)) == expected_titles
    assert result["pagination"]["total"] == len(expected_titles)
    assert result["stats"] == {"total": 5, "pending": 3, "completed": 2}


def test_paginated_stats_ignore_page_size(db, mixed_tasks):
    result = task_service.get_tasks_paginated(db, page=2, page_size=1)

    assert len(result["items"]) == 1
    assert result["stats"] == {"total": 5, "pending": 3, "completed": 2}
