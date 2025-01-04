# app/services/rating/create_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.rating_model import Rating
from app.dtos.rating.requests import CreateRatingDTO
from .validators import validate_rating_data

class CreateRatingService:
    @staticmethod
    async def execute(db: Session, rating_data: CreateRatingDTO) -> Rating:
        try:
            await validate_rating_data(db, rating_data)
            return await CreateRatingService._save_rating(db, rating_data)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def _save_rating(db: Session, rating_data: CreateRatingDTO) -> Rating:
        rating = Rating(**rating_data.model_dump())
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating
