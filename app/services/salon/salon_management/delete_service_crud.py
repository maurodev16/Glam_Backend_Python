# app/services/salon/service_management/delete_service.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from .get_service_crud import GetServiceService

class DeleteServiceService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        service_id: int,
        current_user: User
    ) -> None:
        db_service = await GetServiceService.execute(db, salon_id, service_id)
        db.delete(db_service)
        db.commit()
