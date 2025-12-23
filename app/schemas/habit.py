"""
Pydantic schemas for Habit.
"""

from datetime import datetime

from pydantic import BaseModel


class HabitBase(BaseModel):
    title: str
    description: str | None = None
    is_active: bool = True


class HabitCreate(HabitBase):
    """
    Data for creating a new habit.
    user_id comes from the token, so we do not expose it here.
    """


class HabitRead(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



