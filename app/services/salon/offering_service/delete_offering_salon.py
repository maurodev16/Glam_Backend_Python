# app/services/salon/delete_salon.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from .get_offering_salon import GetOfferingSalonService

class DeleteOfferingSalonService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        current_user: User
    ) -> None:
        salon = await GetOfferingSalonService.execute(db, salon_id)
        db.delete(salon)
        db.commit()
