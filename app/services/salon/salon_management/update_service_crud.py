# app/services/salon/service_management/update_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.models.services_model import Service
from app.dtos.salon_services.requests import UpdateServiceDTO
from .get_service_crud import GetServiceService

logger = logging.getLogger(__name__)

class UpdateServiceService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        service_id: int,
        service_data: UpdateServiceDTO,
        current_user: User
    ) -> Service:
        try:
            db_service = await GetServiceService.execute(db, salon_id, service_id)
            for field, value in service_data.model_dump(exclude_unset=True).items():
                setattr(db_service, field, value)
            db.commit()
            db.refresh(db_service)
            return db_service
        except SQLAlchemyError as e:
            logger.error(f"Error updating service: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating service"
            )
