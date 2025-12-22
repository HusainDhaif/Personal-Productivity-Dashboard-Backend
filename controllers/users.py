from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import UserModel
from serializers.user import UserSignUp, UserSignIn

router = APIRouter()

@router.post("/users/signup")
def sign_up(user: UserSignUp, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = UserModel(
        username=user.username,
        email=user.email
    )
    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    token = new_user.generate_token()
    return {"token": token}

@router.post("/users/signin")
def sign_in(credentials: UserSignIn, db: Session = Depends(get_db)):
    # Find user
    user = db.query(UserModel).filter(
        UserModel.email == credentials.email
    ).first()

    if not user or not user.verify_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    token = user.generate_token()
    return {"token": token}