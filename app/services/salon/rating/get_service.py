# app/services/rating/get_service.py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.rating_model import Rating

class GetRatingService:
    @staticmethod
    async def execute(db: Session, rating_id: int) -> Rating:
        rating = db.query(Rating).filter(Rating.id == rating_id).first()
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rating not found"
            )
        return rating

    @staticmethod
    async def get_salon_ratings(
        db: Session,
        salon_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[Rating]:
        return db.query(Rating)\
            .filter(Rating.salon_id == salon_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
