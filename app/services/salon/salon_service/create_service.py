# app/services/salon/create_salon.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.salon_model import Salon
from app.models.business_hours_model import BusinessHours
from app.models.user_model import User
from app.core.enums.enums import UserRole
from app.dtos.salon.requests import CreateSalonDTO

logger = logging.getLogger(__name__)

class CreateSalonService:
    @staticmethod
    async def execute(
        db: Session,
        salon_data: CreateSalonDTO,
        current_user: User
    ) -> Salon:
        try:
            await CreateSalonService._validate_user_permissions(current_user)
            salon = await CreateSalonService._create_salon(db, salon_data, current_user)
            await CreateSalonService._add_business_hours(db, salon_data, salon.id)
            return salon
        except SQLAlchemyError as e:
            logger.error(f"Database error during salon creation: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating salon"
            )

    @staticmethod
    async def _validate_user_permissions(current_user: User):
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
            **salon_data.model_dump(exclude={'business_hours'}),
            tenant_id=current_user.tenant_id,
            owner_id=current_user.id
        )
        db.add(salon)
        db.flush()
        return salon

    @staticmethod
    async def _add_business_hours(
        db: Session,
        salon_data: CreateSalonDTO,
        salon_id: int
    ):
        if salon_data.business_hours:
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
