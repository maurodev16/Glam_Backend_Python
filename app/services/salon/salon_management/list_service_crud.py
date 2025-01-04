# app/services/salon/service_management/list_service.py
from sqlalchemy.orm import Session
from typing import List

from app.services.salon.salon_service import SalonService

class ListServiceService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[SalonService]:
        return db.query(SalonService)\
            .filter(SalonService.salon_id == salon_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
