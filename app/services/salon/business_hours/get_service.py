# app/services/business_hours/get_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_hours_model import BusinessHours

class GetBusinessHoursService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int
    ) -> BusinessHours:
        hours = db.query(BusinessHours).filter(
            BusinessHours.salon_id == salon_id
        ).first()
        
        if not hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business hours not found"
            )
        return hours
