from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.models.tenant_model import Tenant
from app.dtos.user.requests import UpdateUserDTO

logger = logging.getLogger(__name__)

class UpdateUserService:
    @staticmethod
    async def update_user(
        db: Session,
        user_id: int,
        update_data: UpdateUserDTO
    ) -> User:
        """Update user information"""
        try:
            user = await UpdateUserService._get_user(db, user_id)
            await UpdateUserService._validate_update_data(db, user, update_data)
            return await UpdateUserService._perform_update(db, user, update_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error during user update: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the user"
            )

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
    async def _validate_update_data(
        db: Session,
        user: User,
        update_data: UpdateUserDTO
    ):
        """Validate update data before applying changes"""
        # Validate email uniqueness if being updated
        if update_data.email and update_data.email != user.email:
            if db.query(User).filter(User.email == update_data.email).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Validate phone uniqueness if being updated
        if update_data.phone and update_data.phone != user.phone:
            if db.query(User).filter(User.phone == update_data.phone).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )

        # Validate tenant_id if being updated
        if update_data.tenant_id is not None:
            if update_data.tenant_id == 0:
                update_data.tenant_id = None
            elif update_data.tenant_id is not None:
                tenant = db.query(Tenant).filter(Tenant.id == update_data.tenant_id).first()
                if not tenant:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid tenant_id"
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