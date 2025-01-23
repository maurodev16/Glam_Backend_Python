from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.core.security import get_password_hash
from app.dtos.auth.requests import RegisterUserDTO

logger = logging.getLogger(__name__)

class RegisterService:
    @staticmethod
    async def register_user(
        db: Session, 
        user_data: RegisterUserDTO, 
        tenant_id: Optional[int] = None
    ) -> User:
        """Register a new user"""
        try:
            await RegisterService._validate_unique_fields(db, user_data)
            return await RegisterService._create_user(db, user_data, tenant_id)
        except SQLAlchemyError as e:
            logger.error(f"Database error during registration: {str(e)}")
            db.rollback()
            raise
            #  HTTPException(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     detail="An error occurred while creating the user"
            # )

    @staticmethod
    async def _validate_unique_fields(db: Session, user_data: RegisterUserDTO):
        """Validate unique fields for new user"""
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        if db.query(User).filter(User.phone == user_data.phone).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )

    @staticmethod
    async def _create_user(
        db: Session, 
        user_data: RegisterUserDTO, 
        tenant_id: Optional[int]
    ) -> User:
        """Create new user in database"""
        user = User(
            **user_data.model_dump(exclude={"password"}),
            password=get_password_hash(user_data.password),
            tenant_id=tenant_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"New user registered: {user.email}")
        return user