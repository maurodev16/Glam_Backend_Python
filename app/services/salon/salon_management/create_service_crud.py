# app/services/salon/service_management/create_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.models.services_model import Service as SalonService
from app.dtos.salon_services.requests import CreateServiceDTO

logger = logging.getLogger(__name__)

class CreateServiceService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        service: CreateServiceDTO,
        current_user: User
    ) -> SalonService:
        try:
            db_service = SalonService(
                **service.model_dump(),
                salon_id=salon_id
            )
            db.add(db_service)
            db.commit()
            db.refresh(db_service)
            return db_service
        except SQLAlchemyError as e:
            logger.error(f"Error creating service: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating service"
            )
