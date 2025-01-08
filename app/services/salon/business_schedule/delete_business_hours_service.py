# app/services/business_hours/delete_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import BusinessHours

class DeleteBusinessHoursService:
    @staticmethod
    async def execute(db: Session, hours_id: int) -> None:
        try:
            hours = db.query(BusinessHours).filter(
                BusinessHours.id == hours_id
            ).first()
            
            if not hours:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Business hours not found"
                )
                
            db.delete(hours)
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
