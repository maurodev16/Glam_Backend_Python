# app/services/business_hours/delete_service.py
from sqlalchemy.orm import Session
from .get_service import GetBusinessHoursService

class DeleteBusinessHoursService:
    @staticmethod
    async def execute(db: Session, salon_id: int) -> None:
        hours = await GetBusinessHoursService.execute(db, salon_id)
        db.delete(hours)
        db.commit()
