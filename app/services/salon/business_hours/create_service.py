# app/services/business_hours/create_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_hours_model import BusinessHours
from app.dtos.business_hours.requests import CreateBusinessHoursDTO
from .validators import validate_hours

class CreateBusinessHoursService:
    @staticmethod
    async def execute(
        db: Session, 
        salon_id: int,
        hours_data: CreateBusinessHoursDTO
    ) -> BusinessHours:
        try:
            await validate_hours(hours_data)
            return await CreateBusinessHoursService._save_hours(
                db, salon_id, hours_data
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
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
