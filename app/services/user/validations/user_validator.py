# app/services/user/validations/user_validator.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.dtos.user.requests import UpdateUserDTO
from app.services.tenant.validations.tenant_existence import validate_tenant_id
from .email_validator import validate_email_uniqueness
from .phone_validator import validate_phone_uniqueness

class UserValidator:
    @staticmethod
    async def validate_update_data(
        db: Session,
        user: User,
        update_data: UpdateUserDTO
    ):
        """Validate all user update data"""
        await validate_email_uniqueness(db, user, update_data.email)
        await validate_phone_uniqueness(db, user, update_data.phone)
        await validate_tenant_id(db, update_data.tenant_id)
