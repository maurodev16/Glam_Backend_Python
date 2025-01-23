import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.user_model import User
from app.dtos.salon.requests import CreateSalonDTO
from app.core.enums.enums import UserRole

logger = logging.getLogger(__name__)

class OwnerHandler:
    @staticmethod
    async def handle_owner(
        db: Session,
        current_user: Optional[User],
        salon_data: CreateSalonDTO  # Adicione este argumento
    ) -> User:
        """Ensure current user can be assigned as salon owner"""
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não autenticado."
            )
        
        if current_user.role == UserRole.CLIENT:
            # Update user role to SALON_OWNER
            current_user.role = UserRole.SALON_OWNER
            db.add(current_user)
            db.commit()
            db.refresh(current_user)
        
        return current_user
