# app/services/salon_service/create_service_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.services_model import Service
from app.dtos.salon_services.requests import CreateServiceDTO

logger = logging.getLogger(__name__)

class CreateSalonService:
    @staticmethod
    async def create_salon_service(
        db: Session,
        service_data: CreateServiceDTO
    ) -> Service:
        try:
            await CreateSalonService._validate_service(db, service_data)
            return await CreateSalonService._save_service(db, service_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error creating service: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating service"
            )

    @staticmethod
    async def _validate_salon_service(db: Session, service_data: CreateServiceDTO):
        existing = db.query(Service).filter_by(
            name=service_data.name,
            salon_id=service_data.salon_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service with this name already exists"
            )

    @staticmethod
    async def _save_salon_service(db: Session, service_data: CreateServiceDTO) -> Service:
        service = Service(**service_data.model_dump())
        db.add(service)
        db.commit()
        db.refresh(service)
        return service
