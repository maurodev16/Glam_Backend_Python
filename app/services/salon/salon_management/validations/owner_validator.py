# app/services/salon/validations/owner_validator.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.models.user_model import User
from app.dtos.salon.requests import CreateSalonDTO
from app.core.validators.base_validator import BaseValidator
from app.services.salon.salon_management.owner.owner_creation_service import OwnerCreationService
from .types.owner_validation_types import OwnerValidationData

class OwnerValidator(BaseValidator):
    @staticmethod
    async def validate_owner_data(
        db: Session,
        salon_data: CreateSalonDTO,
        current_user: Optional[User] = None
    ) -> User:
        """Validate owner data and return owner"""
        validation_data = OwnerValidationData(
            salon_data=salon_data,
            current_user=current_user,
            db=db
        )
        
        if salon_data.use_existing_user:
            return await OwnerValidator._validate_existing_user(validation_data)
        return await OwnerValidator._validate_new_owner(validation_data)

    @staticmethod
    async def _validate_existing_user(data: OwnerValidationData) -> User:
        """Validate existing user as owner"""
        if not data.current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required when using existing account"
            )
        return data.current_user

    @staticmethod
    async def _validate_new_owner(data: OwnerValidationData) -> User:
        """Validate and create new owner"""
        required_fields = ['owner_name', 'owner_email', 'owner_phone', 'owner_password']
        if not all(getattr(data.salon_data, field) for field in required_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All owner information is required"
            )

        if not await BaseValidator.validate_unique_field(
            data.db,
            User,
            'email',
            data.salon_data.owner_email
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )

        return await OwnerCreationService.create_owner(data.db, data.salon_data)
