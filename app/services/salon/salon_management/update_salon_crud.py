# app/services/salon/service_management/update_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.models.offering_services_model import OfferingService
from app.dtos.offering_services.requests import UpdateOfferingServiceDTO
from app.services.salon.offering_service.update_offering_salon import UpdateOfferingSalonService

logger = logging.getLogger(__name__)

class UpdateSalonServiceCrud:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        service_id: int,
        service_data: UpdateOfferingServiceDTO,
        current_user: User
    ) -> OfferingService:
        try:
            db_service = await UpdateOfferingSalonService.execute(db, salon_id, service_id, current_user)
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
