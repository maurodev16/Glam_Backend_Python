# app/services/business_hours/update_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.business_schedule_model import BusinessHours
from app.dtos.business_schedule.business_hours.requests import UpdateBusinessHoursRequetsDTO
from app.dtos.business_schedule.business_hours.responses import CreatedBusinessHoursResponseDTO

class UpdateBusinessHoursService:
    @staticmethod
    async def execute(
        db: Session,
        hours_id: int,
        hours_data: UpdateBusinessHoursRequetsDTO
    ) -> CreatedBusinessHoursResponseDTO:
        try:
            hours = db.query(BusinessHours).filter(
                BusinessHours.id == hours_id
            ).first()
            
            if not hours:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Business hours not found"
                )
                
            for field, value in hours_data.model_dump(exclude_unset=True).items():
                setattr(hours, field, value)
                
            db.commit()
            db.refresh(hours)
            return hours
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
