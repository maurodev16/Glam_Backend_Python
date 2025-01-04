# app/services/salon/service_management/get_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.services_model import Service

class GetServiceService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        service_id: int
    ) -> Service:
        service = db.query(Service)\
            .filter(
                Service.salon_id == salon_id,
                Service.id == service_id
            ).first()
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )
        return service
