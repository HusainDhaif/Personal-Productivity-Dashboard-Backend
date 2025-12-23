"""
Pydantic schemas for Note.
"""

from datetime import datetime

from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: str | None = None


class NoteCreate(NoteBase):
    """
    Data for creating a new note.
    user_id comes from the token, so we do not expose it here.
    """


class NoteRead(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



