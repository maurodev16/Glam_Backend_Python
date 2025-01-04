# app/services/salon/update_salon.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.models.salon_model import Salon
from app.dtos.salon.requests import UpdateSalonDTO

logger = logging.getLogger(__name__)

class UpdateSalonService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        salon_data: UpdateSalonDTO,
        current_user: User
    ) -> Salon:
        try:
            salon = await UpdateSalonService.execute(db, salon_id, salon_data, current_user)
            for field, value in salon_data.model_dump(exclude_unset=True).items():
                setattr(salon, field, value)
            db.commit()
            db.refresh(salon)
            return salon
        except SQLAlchemyError as e:
            logger.error(f"Error updating salon: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating salon"
            )
