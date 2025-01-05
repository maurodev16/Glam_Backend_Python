# app/services/salon/list_salon.py
from sqlalchemy.orm import Session
from typing import List
from app.models.salon_model import Salon

class ListOfferingSalonService:
    @staticmethod
    async def execute(
        db: Session,
        skip: int = 0,
        limit: int = 50
    ) -> List[Salon]:
        return db.query(Salon).offset(skip).limit(limit).all()
