# app/services/salon/owner/owner_creation_service.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import get_password_hash
from app.core.enums.enums import UserRole
from app.dtos.salon.requests import CreateSalonDTO

class OwnerCreationService:
    @staticmethod
    async def create_owner(db: Session, salon_data: CreateSalonDTO) -> User:
        """Create new salon owner"""
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
