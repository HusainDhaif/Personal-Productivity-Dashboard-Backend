"""
Pydantic schemas for Task.

These define what data the API accepts and returns for tasks.
"""

from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False


class TaskCreate(TaskBase):
    """
    Data required when creating a new task.
    User is taken from the token, so we don't expose user_id here.
    """


class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



