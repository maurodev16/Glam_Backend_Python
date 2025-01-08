# app/services/salon/update.py
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, logger, status
from app.models.salon_model import Salon
from app.dtos.salon.requests import UpdateSalonDTO
from app.models.user_model import User

class UpdateOfferingSalonService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        salon_data: UpdateSalonDTO,
        current_user: User
    ) -> Salon:
        try:
            # Get salon and verify ownership
            salon = db.query(Salon).filter(Salon.id == salon_id).first()
            if not salon:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Salon not found"
                )
                
            if salon.owner_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only salon owner can update salon"
                )

            # Update salon fields
            for field, value in salon_data.model_dump(exclude_unset=True).items():
                setattr(salon, field, value)
                
            db.commit()
            db.refresh(salon)
            return salon
            
        except Exception as e:
            logger.error(f"Error updating salon: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating salon"
            )
