# app/services/user/delete_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.services.user.get_service import ReadUserService

logger = logging.getLogger(__name__)

class DeleteUserService:
    @staticmethod
    async def delete(db: Session, user_id: int):
        """Delete user"""
        try:
            user = await ReadUserService.get(db, user_id)
            db.delete(user)
            db.commit()
            logger.info(f"Deleted user with ID: {user_id}")
        except SQLAlchemyError as e:
            logger.error(f"Database error deleting user: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting user"
            )
