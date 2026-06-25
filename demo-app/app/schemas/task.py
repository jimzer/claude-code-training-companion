from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    priority: str = "medium"


class TaskCreate(TaskBase):
    user_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    completed: bool | None = None
    user_id: int | None = None


class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime | None
    user_id: int | None

    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class TaskStats(BaseModel):
    total: int
    pending: int
    completed: int


class PaginatedTaskResponse(BaseModel):
    items: list[TaskResponse]
    pagination: PaginationMeta
    stats: TaskStats
