# app/services/business_hours/validators.py
from fastapi import HTTPException, status
from app.dtos.business_hours.requests import CreateBusinessHoursDTO
from sqlalchemy.orm import Session

from app.models.salon_model import Salon
async def validate_hours(hours_data: CreateBusinessHoursDTO):
    """Validate business hours data"""
    if not hours_data.is_closed and hours_data.close_time <= hours_data.open_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid hours for day {hours_data.day_of_week}: close time must be after open time"
        )
        
async def validate_salon_owner(db: Session, salon_id: int, user_id: int):
    """Validate if user is the salon owner"""
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon or salon.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only salon owner can manage business hours"
        )