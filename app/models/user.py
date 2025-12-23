"""
User model for the Personal Productivity Dashboard.

This is a simple SQLAlchemy model with:
- id (primary key)
- email
- password (hashed later – for now just a string field)
"""

from sqlalchemy import Column, Integer, String

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)



