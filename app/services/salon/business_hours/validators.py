# app/services/business_hours/validators.py
from fastapi import HTTPException, status
from app.dtos.business_hours.requests import BaseBusinessHoursDTO

async def validate_hours(hours_data: BaseBusinessHoursDTO):
    """Validate business hours data"""
    for day, hours in hours_data.schedule.items():
        if hours and hours.end <= hours.start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid hours for {day}: end time must be after start time"
            )
