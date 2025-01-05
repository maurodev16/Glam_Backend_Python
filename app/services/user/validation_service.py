from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.dtos.user.requests import UpdateUserDTO
from app.services.salon.salon_management.tenant_validator import TenantValidationService

class UserValidationService:
    @staticmethod
    async def validate_update_data(
        db: Session,
        user: User,
        update_data: UpdateUserDTO
    ):
        """Validate update data before applying changes"""
        await UserValidationService._validate_email(db, user, update_data.email)
        await UserValidationService._validate_phone(db, user, update_data.phone)
        await TenantValidationService.validate_tenant_id(db, update_data.tenant_id)

    @staticmethod
    async def _validate_email(db: Session, user: User, email: str | None):
        """Validate email uniqueness"""
        if email and email != user.email:
            if db.query(User).filter(User.email == email).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

    @staticmethod
    async def _validate_phone(db: Session, user: User, phone: str | None):
        """Validate phone uniqueness"""
        if phone and phone != user.phone:
            if db.query(User).filter(User.phone == phone).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )