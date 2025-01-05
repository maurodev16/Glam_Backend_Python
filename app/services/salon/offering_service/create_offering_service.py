from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.dtos.offering_services.requests import CreateOfferingServiceDTO
from app.models.offering_services_model import OfferingService

class CreateOfferingService:
    @staticmethod
    async def execute(db: Session, service_data: CreateOfferingServiceDTO) -> OfferingService:
        """Create a new service"""
        service = OfferingService(**service_data.model_dump())
        db.add(service)
        db.commit()
        db.refresh(service)
        return service