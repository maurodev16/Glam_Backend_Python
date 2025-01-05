# app/services/salon/service_management/delete_service.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.services.salon.offering_service.delete_offering_salon import DeleteOfferingSalonService

class DeleteSalonServiceCrud:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        service_id: int,
        current_user: User
    ) -> None:
        db_service = await DeleteOfferingSalonService.execute(db, salon_id, service_id)
        db.delete(db_service)
        db.commit()
