from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.core.security import verify_password, get_password_hash

logger = logging.getLogger(__name__)

class PasswordService:
    @staticmethod
    async def update_password(
        db: Session, 
        user_id: int, 
        current_password: str,
        new_password: str
    ):
        """Update user password"""
        try:
            user = await PasswordService._get_user(db, user_id)
            await PasswordService._validate_current_password(user, current_password)
            await PasswordService._set_new_password(db, user, new_password)
        except Exception as e:
            logger.error(f"Password update error: {str(e)}")
            raise

    @staticmethod
    async def _get_user(db: Session, user_id: int) -> User:
        """Get user by ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    async def _validate_current_password(user: User, current_password: str):
        """Validate current password"""
        if not verify_password(current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )

    @staticmethod
    async def _set_new_password(db: Session, user: User, new_password: str):
        """Set new password"""
        user.password = get_password_hash(new_password)
        db.commit()