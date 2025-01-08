# app/services/salon/get_salon.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.salon_model import Salon
from typing import Optional

class GetOfferingSalonService:
    @staticmethod
    async def execute(db: Session, salon_id: int, check_active: bool = True) -> Salon:
        """Get salon by ID"""
        try:
            query = db.query(Salon).filter(Salon.id == salon_id)
            
            if check_active:
                query = query.filter(Salon.is_active == True)
                
            salon = query.first()
            
            if not salon:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Salon not found"
                )
                
            return salon
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
