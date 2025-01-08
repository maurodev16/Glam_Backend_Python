# app/services/business_hours/get_service.py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import BusinessHours

class GetBusinessHoursService:
    @staticmethod
    async def get_by_id(db: Session, hours_id: int) -> BusinessHours:
        hours = db.query(BusinessHours).filter(
            BusinessHours.id == hours_id
        ).first()
        
        if not hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business hours not found"
            )
        return hours

    @staticmethod
    async def get_all(db: Session, salon_id: int) -> List[BusinessHours]:
        return db.query(BusinessHours).filter(
            BusinessHours.salon_id == salon_id
        ).all()
