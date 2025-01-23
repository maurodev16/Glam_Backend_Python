# app/services/business_hours/validators.py
from datetime import time
from fastapi import HTTPException, status
from app.dtos.business_schedule.business_hours.requests import CreateBusinessHoursRequestDTO 

from sqlalchemy.orm import Session

from app.models.salon_model import Salon
async def validate_hours(hours_data: CreateBusinessHoursRequestDTO):
    """Validate business hours data"""
    if not hours_data.is_closed:
        try:
            open_time = time.fromisoformat(hours_data.open_time)
            close_time = time.fromisoformat(hours_data.close_time)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid time format. Use HH:MM"
            )

        if close_time <= open_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid hours for day {hours_data.day_of_week_id}: close time must be after open time"
            )
        
async def validate_salon_owner(db: Session, salon_id: int, user_id: int):
    """Validate if user is the salon owner"""
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salon not found"
        )
    if salon.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only salon owner can manage employees"
        )
    return salon