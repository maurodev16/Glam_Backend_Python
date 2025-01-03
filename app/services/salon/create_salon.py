from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging
from typing import Optional

from app.models.salon_model import Salon
from app.models.business_hours_model import BusinessHours
from app.models.user_model import User
from app.core.enums.enums import UserRole
from app.dtos.salon.requests import CreateSalonDTO
from app.dtos.business_hours.requests import CreateBusinessHoursDTO

logger = logging.getLogger(__name__)

class CreateSalon:
    @staticmethod
    async def create_salon(
        db: Session,
        salon_data: CreateSalonDTO,
        current_user: User
    ) -> Salon:
        """Create a new salon"""
        try:
            CreateSalon._validate_user_permissions(current_user)
            db_salon = await CreateSalon._create_salon(db, salon_data, current_user)
            await CreateSalon._add_business_hours(db, salon_data, db_salon.id)
            return db_salon
        except SQLAlchemyError as e:
            logger.error(f"Database error during salon registration: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the salon"
            )

    @staticmethod
    def _validate_user_permissions(current_user: User):
        """Validate if the user has permissions to register a salon"""
        if current_user.role not in [UserRole.CLIENT, UserRole.SALON_OWNER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only salon owners or admins can create a salon"
            )

    @staticmethod
    async def _create_salon(
        db: Session,
        salon_data: CreateSalonDTO,
        current_user: User
    ) -> Salon:
        salon = Salon(
            **salon_data.model_dump(exclude={'business_hours'}),  # Changed from business_hours_model
            tenant_id=current_user.tenant_id,
            owner_id=current_user.id  # Added owner_id
        )
        db.add(salon)
        db.flush()
        logger.info(f"Salon created: {salon.name} (ID: {salon.id})")
        return salon

    @staticmethod
    async def _add_business_hours(
        db: Session,
        salon_data: CreateSalonDTO, 
        salon_id: int
    ) -> BusinessHours:
        if salon_data.business_hours:  # Changed from business_hours_model
            for hours_data in salon_data.business_hours:
                business_hours = BusinessHours(
                    salon_id=salon_id,
                    day_of_week=hours_data.day_of_week,
                    open_time=hours_data.open_time,
                    close_time=hours_data.close_time,
                    is_closed=hours_data.is_closed
                )
                db.add(business_hours)
        db.commit()
