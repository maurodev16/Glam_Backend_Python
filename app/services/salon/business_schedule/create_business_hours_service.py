# app/services/business_hours/create_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import BusinessDay, BusinessHours
from app.dtos.business_hours.requests import CreateBusinessHoursDTO

class CreateBusinessHoursService:
    @staticmethod
    async def execute(db: Session, salon_id: int, hours_data: CreateBusinessHoursDTO) -> BusinessHours:
        try:
            # Create or get business day
            business_day = await CreateBusinessHoursService._get_or_create_business_day(
                db, salon_id, hours_data.day_of_week
            )
            
            # Create business hours
            hours = BusinessHours(
                salon_id=salon_id,
                business_day_id=business_day.id,
                open_time=hours_data.open_time,
                close_time=hours_data.close_time
            )
            
            db.add(hours)
            db.commit()
            db.refresh(hours)
            return hours
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def _get_or_create_business_day(
        db: Session, 
        salon_id: int, 
        day_of_week: int
    ) -> BusinessDay:
        business_day = db.query(BusinessDay).filter(
            BusinessDay.salon_id == salon_id,
            BusinessDay.day_of_week == day_of_week
        ).first()
        
        if not business_day:
            business_day = BusinessDay(
                salon_id=salon_id,
                day_of_week=day_of_week
            )
            db.add(business_day)
            db.flush()
            
        return business_day
