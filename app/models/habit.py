"""
Habit model for the Personal Productivity Dashboard.

Linked to the existing UserModel via user_id.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from models.base import BaseModel
from models.user import UserModel


class Habit(BaseModel):
    __tablename__ = "habits"

    # Inherits id, created_at, updated_at from BaseModel
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Optional relationship back to the user
    user = relationship(UserModel, backref="habits")



