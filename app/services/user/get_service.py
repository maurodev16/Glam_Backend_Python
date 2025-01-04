# app/services/user/get_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging
from typing import List
from app.models.user_model import User
from app.core.enums.enums import StatusRole

logger = logging.getLogger(__name__)

class ReadUserService:
    @staticmethod
    async def get(db: Session, user_id: int) -> User:
        """Get user by ID"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving user"
            )

    @staticmethod
    async def list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        is_active: bool = True
    ) -> List[User]:
        """List users with optional filtering"""
        try:
            query = db.query(User)
            if is_active:
                query = query.filter(User.is_active == StatusRole.ACTIVE)
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error listing users: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error listing users"
            )
