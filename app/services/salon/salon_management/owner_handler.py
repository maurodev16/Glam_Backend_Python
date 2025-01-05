import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.user_model import User
from app.dtos.salon.requests import CreateSalonDTO
from app.core.security import get_password_hash
from app.core.enums.enums import UserRole

logger = logging.getLogger(__name__)

class OwnerHandler:
    @staticmethod
    async def handle_owner(
        db: Session,
        salon_data: CreateSalonDTO,
        current_user: Optional[User]
    ) -> User:
        """Handle salon owner creation or validation"""
        if salon_data.use_existing_user:
            return await OwnerHandler._validate_existing_user(db, current_user)
        return await OwnerHandler._create_new_owner(db, salon_data)

    @staticmethod
    async def _validate_existing_user(db: Session, current_user: Optional[User]) -> User:
        """Validate existing user for salon ownership"""
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must be logged in to use existing account"
            )
        return current_user

    @staticmethod
    async def _create_new_owner(db: Session, salon_data: CreateSalonDTO) -> User:
        """Create new user as salon owner"""
        if not all([
            salon_data.owner_name,
            salon_data.owner_email,
            salon_data.owner_phone,
            salon_data.owner_password
        ]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner information required for new user"
            )

        # Check if email is already in use
        if db.query(User).filter(User.email == salon_data.owner_email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )

        owner = User(
            name=salon_data.owner_name,
            email=salon_data.owner_email,
            phone=salon_data.owner_phone,
            password=get_password_hash(salon_data.owner_password),
            role=UserRole.SALON_OWNER
        )
        db.add(owner)
        db.flush()
        return owner