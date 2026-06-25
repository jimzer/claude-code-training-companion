from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_path: str = "tasks.db"
    app_name: str = "Task Manager"
    debug: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
