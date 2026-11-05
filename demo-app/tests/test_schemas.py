"""Pydantic rules, tested on the models directly (no HTTP)."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.task import (
    PaginatedTaskResponse,
    PaginationMeta,
    TaskCreate,
    TaskResponse,
    TaskStats,
    TaskUpdate,
)
from app.schemas.user import UserCreate, UserResponse

TIMESTAMP = "2026-01-02T03:04:05+00:00"
PARSED_TIMESTAMP = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)

TASK_RESPONSE_DATA = {
    "id": 1,
    "title": "Task",
    "completed": False,
    "created_at": TIMESTAMP,
    "updated_at": None,
    "user_id": None,
}
PAGINATION_DATA = {
    "page": 1,
    "page_size": 20,
    "total": 1,
    "total_pages": 1,
    "has_next": False,
    "has_previous": False,
}
STATS_DATA = {"total": 1, "pending": 1, "completed": 0}
USER_CREATE_DATA = {"username": "alice", "email": "alice@example.com"}
USER_RESPONSE_DATA = {**USER_CREATE_DATA, "id": 1, "created_at": TIMESTAMP}


def without(data, field):
    return {key: value for key, value in data.items() if key != field}


def assert_rejected(model, data, error_type, *loc):
    """Check that validation fails once, at this location, for this reason."""
    with pytest.raises(ValidationError) as exc_info:
        model.model_validate(data)
    errors = exc_info.value.errors()
    assert [(error["loc"], error["type"]) for error in errors] == [(loc, error_type)]


# TaskCreate


def test_task_create_only_requires_title():
    task = TaskCreate(title="Task")
    assert task.title == "Task"
    assert task.description is None
    assert task.priority == "medium"
    assert task.user_id is None


def test_task_create_rejects_missing_title():
    assert_rejected(TaskCreate, {}, "missing", "title")


@pytest.mark.parametrize(
    ("field", "value", "error_type"),
    [
        ("title", None, "string_type"),
        ("title", 123, "string_type"),
        ("description", 123, "string_type"),
        ("priority", None, "string_type"),
        ("user_id", "abc", "int_parsing"),
    ],
)
def test_task_create_rejects_wrong_types(field, value, error_type):
    assert_rejected(TaskCreate, {"title": "Task", field: value}, error_type, field)


@pytest.mark.xfail(
    strict=True,
    raises=pytest.fail.Exception,
    reason=(
        "TaskCreate.priority accepts any string, while GET /tasks/ only filters on "
        "low, medium and high, so such a task cannot be found by its priority"
    ),
)
def test_task_create_rejects_unknown_priority():
    with pytest.raises(ValidationError):
        TaskCreate.model_validate({"title": "Task", "priority": "urgent"})


# TaskUpdate and exclude_unset


def test_task_update_has_no_required_field():
    assert TaskUpdate().model_dump() == {
        "title": None,
        "description": None,
        "priority": None,
        "completed": None,
        "user_id": None,
    }


def test_task_update_exclude_unset_is_empty_when_nothing_is_sent():
    assert TaskUpdate().model_dump(exclude_unset=True) == {}


def test_task_update_exclude_unset_keeps_only_sent_fields():
    update = TaskUpdate.model_validate({"title": "New", "completed": False})
    assert update.model_dump(exclude_unset=True) == {
        "title": "New",
        "completed": False,
    }


@pytest.mark.parametrize("field", ["description", "user_id"])
def test_task_update_exclude_unset_keeps_explicit_null(field):
    update = TaskUpdate.model_validate({field: None})
    assert update.model_dump(exclude_unset=True) == {field: None}


def test_task_update_ignores_unknown_fields():
    update = TaskUpdate.model_validate({"title": "New", "unknown": "value"})
    assert update.model_dump(exclude_unset=True) == {"title": "New"}


@pytest.mark.parametrize(
    ("field", "value", "error_type"),
    [
        ("title", 123, "string_type"),
        ("description", 123, "string_type"),
        ("priority", 123, "string_type"),
        ("completed", "maybe", "bool_parsing"),
        ("user_id", "abc", "int_parsing"),
    ],
)
def test_task_update_rejects_wrong_types(field, value, error_type):
    assert_rejected(TaskUpdate, {field: value}, error_type, field)


@pytest.mark.xfail(
    strict=True,
    raises=pytest.fail.Exception,
    reason=(
        "TaskUpdate accepts null on non-nullable fields and update_task writes it: "
        "title makes PATCH return 500, priority also makes GET /tasks/ return 500 "
        "from then on, completed drops the task from status=pending and the stats"
    ),
)
@pytest.mark.parametrize("field", ["title", "priority", "completed"])
def test_task_update_rejects_null_on_non_nullable_field(field):
    with pytest.raises(ValidationError):
        TaskUpdate.model_validate({field: None})


@pytest.mark.xfail(
    strict=True,
    raises=pytest.fail.Exception,
    reason=(
        "TaskUpdate.priority accepts any string, while GET /tasks/ only filters on "
        "low, medium and high, so such a task cannot be found by its priority"
    ),
)
def test_task_update_rejects_unknown_priority():
    with pytest.raises(ValidationError):
        TaskUpdate.model_validate({"priority": "urgent"})


# TaskResponse


def test_task_response_applies_defaults_and_allows_null():
    task = TaskResponse.model_validate(TASK_RESPONSE_DATA)
    assert task.description is None
    assert task.priority == "medium"
    assert task.updated_at is None
    assert task.user_id is None


def test_task_response_parses_timestamps():
    data = {**TASK_RESPONSE_DATA, "updated_at": TIMESTAMP}
    task = TaskResponse.model_validate(data)
    assert task.created_at == PARSED_TIMESTAMP
    assert task.updated_at == PARSED_TIMESTAMP


@pytest.mark.parametrize("field", list(TASK_RESPONSE_DATA))
def test_task_response_requires_field(field):
    data = without(TASK_RESPONSE_DATA, field)
    assert_rejected(TaskResponse, data, "missing", field)


@pytest.mark.parametrize(
    ("field", "error_type"),
    [
        ("id", "int_type"),
        ("title", "string_type"),
        ("priority", "string_type"),
        ("completed", "bool_type"),
        ("created_at", "datetime_type"),
    ],
)
def test_task_response_non_nullable_fields_reject_null(field, error_type):
    data = {**TASK_RESPONSE_DATA, field: None}
    assert_rejected(TaskResponse, data, error_type, field)


# Pagination envelope


@pytest.mark.parametrize("field", list(PAGINATION_DATA))
def test_pagination_meta_requires_field(field):
    assert_rejected(PaginationMeta, without(PAGINATION_DATA, field), "missing", field)


@pytest.mark.parametrize("field", list(STATS_DATA))
def test_task_stats_requires_field(field):
    assert_rejected(TaskStats, without(STATS_DATA, field), "missing", field)


def test_paginated_response_validates_nested_models():
    response = PaginatedTaskResponse.model_validate(
        {
            "items": [TASK_RESPONSE_DATA],
            "pagination": PAGINATION_DATA,
            "stats": STATS_DATA,
        }
    )
    assert isinstance(response.items[0], TaskResponse)
    assert isinstance(response.pagination, PaginationMeta)
    assert isinstance(response.stats, TaskStats)


def test_paginated_response_rejects_invalid_item():
    data = {
        "items": [without(TASK_RESPONSE_DATA, "updated_at")],
        "pagination": PAGINATION_DATA,
        "stats": STATS_DATA,
    }
    assert_rejected(PaginatedTaskResponse, data, "missing", "items", 0, "updated_at")


# Users


@pytest.mark.parametrize("field", list(USER_CREATE_DATA))
def test_user_create_requires_field(field):
    assert_rejected(UserCreate, without(USER_CREATE_DATA, field), "missing", field)


@pytest.mark.parametrize("field", list(USER_RESPONSE_DATA))
def test_user_response_requires_field(field):
    data = without(USER_RESPONSE_DATA, field)
    assert_rejected(UserResponse, data, "missing", field)


def test_user_response_parses_created_at():
    user = UserResponse.model_validate(USER_RESPONSE_DATA)
    assert user.created_at == PARSED_TIMESTAMP
