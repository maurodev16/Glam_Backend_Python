# app/services/business_hours/create_business_hours_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.business_hours_model import BusinessHours
from app.dtos.business_hours.requests import CreateBusinessHoursDTO

logger = logging.getLogger(__name__)

class CreateBusinessHoursService:
    @staticmethod
    async def create_business_hours(
        db: Session, 
        salon_id: int,
        hours_data: CreateBusinessHoursDTO
    ) -> BusinessHours:
        try:
            await CreateBusinessHoursService._validate_hours(hours_data)
            return await CreateBusinessHoursService._save_hours(db, salon_id, hours_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error creating business hours: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating business hours"
            )

    @staticmethod
    async def _validate_hours(hours_data: CreateBusinessHoursDTO):
        for day, hours in hours_data.schedule.items():
            if hours and hours.end <= hours.start:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid hours for {day}: end time must be after start time"
                )

    @staticmethod
    async def _save_hours(
        db: Session,
        salon_id: int,
        hours_data: CreateBusinessHoursDTO
    ) -> BusinessHours:
        hours = BusinessHours(
            salon_id=salon_id,
            **hours_data.model_dump()
        )
        db.add(hours)
        db.commit()
        db.refresh(hours)
        return hours
