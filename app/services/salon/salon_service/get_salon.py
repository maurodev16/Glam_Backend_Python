# app/services/salon/get_salon.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.salon_model import Salon


class GetSalonService:
    @staticmethod
    async def execute(db: Session, salon_id: int) -> Salon:
        salon = db.query(Salon).filter(Salon.id == salon_id).first()
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found"
            )
        return salon
