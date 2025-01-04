# app/services/business_hours/update_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_hours_model import BusinessHours
from app.dtos.business_hours.requests import UpdateBusinessHoursDTO
from .validators import validate_hours
from .get_service import GetBusinessHoursService

class UpdateBusinessHoursService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        hours_data: UpdateBusinessHoursDTO
    ) -> BusinessHours:
        try:
            hours = await GetBusinessHoursService.execute(db, salon_id)
            await validate_hours(hours_data)
            return await UpdateBusinessHoursService._update_hours(
                db, hours, hours_data
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def _update_hours(
        db: Session,
        hours: BusinessHours,
        hours_data: UpdateBusinessHoursDTO
    ) -> BusinessHours:
        for field, value in hours_data.model_dump(exclude_unset=True).items():
            setattr(hours, field, value)
            
        db.commit()
        db.refresh(hours)
        return hours
