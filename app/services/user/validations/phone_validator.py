# app/services/user/validations/phone_validator.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User

async def validate_phone_uniqueness(db: Session, user: User, phone: str | None):
    """Validate phone uniqueness"""
    if phone and phone != user.phone:
        if db.query(User).filter(User.phone == phone).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
