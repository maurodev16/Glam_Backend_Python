from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import BusinessDay, DayOfWeek
from app.dtos.business_schedule.business_day.requests import  DayOfWeekRequestDTO
from app.dtos.business_schedule.business_day.responses import DayOfWeekResponseDTO

# Service
class CreateDayOfWeekService:
    @staticmethod
    async def execute(db: Session, day_data: DayOfWeekRequestDTO) -> DayOfWeekResponseDTO:
        try:
            existing_day = db.query(DayOfWeek).filter(
                DayOfWeek.day_name == day_data.day_name
            ).first()

            if existing_day:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Day of week '{day_data.day_name}' already exists."
                )

            day_of_week = DayOfWeek(day_name=day_data.day_name)
            db.add(day_of_week)
            db.commit()
            db.refresh(day_of_week)
            
            return day_of_week
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )