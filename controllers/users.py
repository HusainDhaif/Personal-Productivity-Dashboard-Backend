import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from models.user import UserModel
from serializers.user import UserSignUp, UserSignIn, AuthResponse

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["authentication"])

@router.post("/register/", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserSignUp, request: Request, db: Session = Depends(get_db)):
    """
    Register a new user.
    Accepts JSON with username, email, and password.
    Returns JWT token on success.
    """
    try:
        logger.info(f"Registration attempt for email: {user.email} from {request.client.host}")
        
        # Check if user already exists
        existing_user = db.query(UserModel).filter(
            UserModel.email == user.email
        ).first()

        if existing_user:
            logger.warning(f"Registration failed: Email {user.email} already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check if username already exists
        existing_username = db.query(UserModel).filter(
            UserModel.username == user.username
        ).first()

        if existing_username:
            logger.warning(f"Registration failed: Username {user.username} already taken")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

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
        logger.info(f"User registered successfully: {user.email} (ID: {new_user.id})")
        
        return {
            "token": token,
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error for {user.email}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )

@router.post("/login/", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(credentials: UserSignIn, request: Request, db: Session = Depends(get_db)):
    """
    Login with email and password.
    Accepts JSON with email and password.
    Returns JWT token on success.
    """
    try:
        logger.info(f"Login attempt for email: {credentials.email} from {request.client.host}")
        
        # Find user
        user = db.query(UserModel).filter(
            UserModel.email == credentials.email
        ).first()

        if not user:
            logger.warning(f"Login failed: User with email {credentials.email} not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not user.verify_password(credentials.password):
            logger.warning(f"Login failed: Invalid password for email {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Generate JWT token
        token = user.generate_token()
        logger.info(f"User logged in successfully: {credentials.email} (ID: {user.id})")
        
        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {credentials.email}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )