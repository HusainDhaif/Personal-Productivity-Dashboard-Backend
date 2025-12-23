"""
Note model for the Personal Productivity Dashboard.

Linked to the existing UserModel via user_id.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.user import UserModel


class Note(BaseModel):
    __tablename__ = "notes"

    # Inherits id, created_at, updated_at from BaseModel
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Optional relationship back to the user
    user = relationship(UserModel, backref="notes")



