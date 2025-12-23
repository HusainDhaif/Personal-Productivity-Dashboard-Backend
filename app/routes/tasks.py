"""
Task routes (CRUD) for the Personal Productivity Dashboard.

All routes are protected using the existing JWT `get_current_user` dependency.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.user import UserModel
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create a new task for the logged-in user.
    """
    task = Task(
        title=task_in.title,
        description=task_in.description,
        is_completed=task_in.is_completed,
        user_id=current_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/", response_model=List[TaskRead])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Get all tasks that belong to the logged-in user.
    """
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update an existing task that belongs to the logged-in user.
    """
    task = db.query(Task).filter(
        Task.id == task_id, Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.title = task_in.title
    task.description = task_in.description
    task.is_completed = task_in.is_completed

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Delete a task that belongs to the logged-in user.
    """
    task = db.query(Task).filter(
        Task.id == task_id, Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    # No content to return for a successful delete
    return None



