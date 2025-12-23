"""
Habit routes (CRUD) for the Personal Productivity Dashboard.

All routes are protected using the existing JWT `get_current_user` dependency.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.user import UserModel
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitRead

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_in: HabitCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create a new habit for the logged-in user.
    """
    habit = Habit(
        title=habit_in.title,
        description=habit_in.description,
        is_active=habit_in.is_active,
        user_id=current_user.id,
    )

    db.add(habit)
    db.commit()
    db.refresh(habit)

    return habit


@router.get("/", response_model=List[HabitRead])
def get_my_habits(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Get all habits that belong to the logged-in user.
    """
    habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()
    return habits


@router.put("/{habit_id}", response_model=HabitRead)
def update_habit(
    habit_id: int,
    habit_in: HabitCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update an existing habit that belongs to the logged-in user.
    """
    habit = db.query(Habit).filter(
        Habit.id == habit_id, Habit.user_id == current_user.id
    ).first()

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    habit.title = habit_in.title
    habit.description = habit_in.description
    habit.is_active = habit_in.is_active

    db.commit()
    db.refresh(habit)

    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Delete a habit that belongs to the logged-in user.
    """
    habit = db.query(Habit).filter(
        Habit.id == habit_id, Habit.user_id == current_user.id
    ).first()

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    db.delete(habit)
    db.commit()

    # No content to return for a successful delete
    return None



