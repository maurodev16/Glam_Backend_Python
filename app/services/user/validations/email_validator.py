# app/services/user/validations/email_validator.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User

async def validate_email_uniqueness(db: Session, user: User, email: str | None):
    """Validate email uniqueness"""
    if email and email != user.email:
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
