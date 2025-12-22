from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models