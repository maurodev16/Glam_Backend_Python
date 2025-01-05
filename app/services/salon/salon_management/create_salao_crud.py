from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import Optional
import logging

from app.models.user_model import User
from app.models.salon_model import Salon
from app.dtos.salon.requests import CreateSalonDTO
from app.services.salon.salon_management.tenant_handler import TenantHandler
from .tenant_validator import TenantValidationService
from .owner_handler import OwnerHandler
from .salon_creator import SalonCreator

logger = logging.getLogger(__name__)

# app/services/salon/create/create_salon_service.py
class CreateSalonServiceCrud:
    @staticmethod
    async def execute(
        db: Session,
        salon_data: CreateSalonDTO,
        current_user: Optional[User] = None
    ) -> Salon:
        """Orchestrate salon creation process"""
        try:
            # Handle owner creation/validation first
            owner = await OwnerHandler.handle_owner(db, salon_data, current_user)
            
            # Handle tenant creation/validation
            tenant = await TenantHandler.handle_tenant(db, salon_data, owner)
            
            # Create salon and related records
            salon = await SalonCreator.create_salon(db, salon_data, owner, tenant)
            
            db.commit()
            return salon
            
        except SQLAlchemyError as e:
            logger.error(f"Database error creating salon: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating salon"
            )
