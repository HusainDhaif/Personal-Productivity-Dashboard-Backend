"""
Pydantic schemas for the User model.

These are used to define what data is accepted/returned by the API.
For now we keep it very simple for learning purposes.
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True



