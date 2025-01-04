# app/services/user/update_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.dtos.user.requests import UpdateUserDTO
from .validation_service import UserValidationService
from .get_service import ReadUserService

logger = logging.getLogger(__name__)

class UpdateUserService:
    @staticmethod
    async def update(
        db: Session,
        user_id: int,
        update_data: UpdateUserDTO
    ) -> User:
        """Update user information"""
        try:
            user = await ReadUserService.get(db, user_id)
            await UserValidationService.validate_update_data(db, user, update_data)
            return await UpdateUserService._perform_update(db, user, update_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error during user update: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the user"
            )

    @staticmethod
    async def _perform_update(
        db: Session,
        user: User,
        update_data: UpdateUserDTO
    ) -> User:
        """Apply updates to user"""
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user
