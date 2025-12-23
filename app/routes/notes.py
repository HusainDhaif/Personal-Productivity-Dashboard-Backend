"""
Note routes (CRUD) for the Personal Productivity Dashboard.

All routes are protected using the existing JWT `get_current_user` dependency.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.user import UserModel
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create a new note for the logged-in user.
    """
    note = Note(
        title=note_in.title,
        content=note_in.content,
        user_id=current_user.id,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


@router.get("/", response_model=List[NoteRead])
def get_my_notes(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Get all notes that belong to the logged-in user.
    """
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return notes


@router.put("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    note_in: NoteCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Update an existing note that belongs to the logged-in user.
    """
    note = db.query(Note).filter(
        Note.id == note_id, Note.user_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.title = note_in.title
    note.content = note_in.content

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Delete a note that belongs to the logged-in user.
    """
    note = db.query(Note).filter(
        Note.id == note_id, Note.user_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()

    # No content to return for a successful delete
    return None



