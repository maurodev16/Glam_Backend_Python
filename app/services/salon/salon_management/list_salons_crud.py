# app/services/salon/service_management/list_service.py
from sqlalchemy.orm import Session
from typing import List

from app.models.offering_services_model import OfferingService

class ListSalonServiceCrud:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[OfferingService]:
        return db.query(OfferingService)\
            .filter(OfferingService.salon_id == salon_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
