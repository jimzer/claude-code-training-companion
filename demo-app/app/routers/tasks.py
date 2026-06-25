import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query

from app.db import get_db
from app.schemas.task import PaginatedTaskResponse, TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=PaginatedTaskResponse)
def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = Query(None, pattern=r"^(pending|completed)$"),
    priority: str | None = Query(None, pattern=r"^(low|medium|high)$"),
    db: sqlite3.Connection = Depends(get_db),
):
    return task_service.get_tasks_paginated(db, page, page_size, status, priority)


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: sqlite3.Connection = Depends(get_db)):
    return task_service.create_task(db, task_data)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, task_data: TaskUpdate, db: sqlite3.Connection = Depends(get_db)
):
    task = task_service.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    task = task_service.complete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
