from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import BusinessHours
from app.dtos.business_schedule.business_hours.responses import CreatedBusinessHoursResponseDTO

class GetBusinessHoursService:
    @staticmethod
    async def get_by_id(db: Session, hours_id: int) -> CreatedBusinessHoursResponseDTO:
        """Get business hours by ID"""
        hours = db.query(BusinessHours).filter(
            BusinessHours.id == hours_id
        ).first()
        
        if not hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business hours not found"
            )

        # Mapear para o modelo Pydantic
        return CreatedBusinessHoursResponseDTO(
            id=hours.id,
            salon_id=hours.salon_id,
            business_day_id=hours.business_day_id,
            open_time=hours.open_time.strftime("%H:%M"),
            close_time=hours.close_time.strftime("%H:%M")
        )

    @staticmethod
    async def get_all(db: Session, salon_id: int, day_of_week: Optional[int] = None) -> List[CreatedBusinessHoursResponseDTO]:
        """Get all business hours, optionally filtering by day of the week"""
        query = db.query(BusinessHours).filter(
            BusinessHours.salon_id == salon_id
        )

        if day_of_week is not None:
            query = query.filter(BusinessHours.business_day_id == day_of_week)

        business_hours = query.all()

        # Mapear para o modelo Pydantic
        return [
            CreatedBusinessHoursResponseDTO(
                id=item.id,
                salon_id=item.salon_id,
                day_of_week_id=item.business_day_id,
                open_time=item.open_time.strftime("%H:%M"),
                close_time=item.close_time.strftime("%H:%M"),
            )
            for item in business_hours
        ]
