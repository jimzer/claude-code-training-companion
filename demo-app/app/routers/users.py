import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def list_users(db: sqlite3.Connection = Depends(get_db)):
    return user_service.get_users(db)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    return user_service.create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
