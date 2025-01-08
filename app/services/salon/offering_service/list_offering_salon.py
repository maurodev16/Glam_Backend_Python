# app/services/salon/list_salon.py
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from app.models.salon_model import Salon

class ListOfferingSalonService:
    @staticmethod
    async def execute(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        only_active: bool = True
    ) -> List[Salon]:
        """List salons with pagination"""
        try:
            query = db.query(Salon)
            
            if only_active:
                query = query.filter(Salon.is_active == True)
                
            return query.order_by(Salon.created_at.desc())\
                       .offset(skip)\
                       .limit(limit)\
                       .all()
                       
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=str(e)
            )
