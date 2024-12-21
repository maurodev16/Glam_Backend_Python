# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
import logging

from ..core.enums.enums import StatusRole

from ..core.database import get_db
from ..models import user_model as models
from ..schemas import user_schema as schemas
from ..core.security import SecurityService
from ..core.config import get_settings
settings = get_settings()

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        401: {"description": "Authentication failed"},
        403: {"description": "Forbidden"},
        404: {"description": "Resource not found"}
    }
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthenticationError(HTTPException):
    """Custom exception for authentication errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> models.User:
    """
    Dependency to get the current authenticated user.
    Validates the JWT token and returns the user if valid.
    """
    try:
        payload = SecurityService.decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationError("Invalid authentication token")
            
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise AuthenticationError("User not found")
            
        if not user.is_active == StatusRole.INACTIVE:  # Assuming you have an is_active field
            raise AuthenticationError("Inactive user")
            
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise AuthenticationError("Authentication failed")

@router.post(
    "/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid request or email already exists"}
    }
)
async def register(
    user: schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)]
):
    """Register a new user"""
    try:
        # Check if email already exists
        if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        db_user = models.User(
            **user.model_dump(exclude={"password"}),
            password=SecurityService.get_password_hash(user.password)
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"New user registered: {user.email}")
        return db_user
        
    except SQLAlchemyError as e:
        logger.error(f"Database error during registration: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@router.post(
    "/login",
    response_model=schemas.Token,
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Login failed"}
    }
)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """Authenticate user and return JWT token"""
    try:
        # Find user by email
        user = db.query(models.User).filter(models.User.email == form_data.username).first()
        
        # Verify user and password
        if not user or not SecurityService.verify_password(form_data.password, user.password):
            raise AuthenticationError("Incorrect email or password")
            
        if not user.is_active != StatusRole.INACTIVE:
            raise AuthenticationError("User account is inactive")
        
        # Create access token
        access_token = SecurityService.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        # Optional: Set cookie with token
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        logger.info(f"User logged in: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise AuthenticationError("Authentication failed")

@router.get(
    "/me",
    response_model=schemas.User,
    responses={
        200: {"description": "Current user information"},
        401: {"description": "Not authenticated"}
    }
)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    """Get current authenticated user information"""
    return current_user

@router.post("/logout")
async def logout(response: Response):
    """Logout current user"""
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax"
    )
    return {"message": "Successfully logged out"}