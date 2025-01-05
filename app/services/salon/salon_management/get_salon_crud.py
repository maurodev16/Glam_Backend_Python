# app/services/salon/service_management/get_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.offering_services_model import OfferingService

class GetSalonServiceCrud:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        service_id: int
    ) -> OfferingService:
        salon = db.query(OfferingService)\
            .filter(
                OfferingService.salon_id == salon_id,
                OfferingService.id == service_id
            ).first()
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )
        return salon
