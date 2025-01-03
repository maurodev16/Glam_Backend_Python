# app/services/rating/create_rating_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.rating_model import Rating
from app.dtos.rating.requests import CreateRatingDTO
from app.models.salon_model import Salon

logger = logging.getLogger(__name__)

class CreateRatingService:
    @staticmethod
    async def create_rating(db: Session, rating_data: CreateRatingDTO) -> Rating:
        """Create a new rating"""
        try:
            await CreateRatingService._validate_rating(db, rating_data)
            return await CreateRatingService._save_rating(db, rating_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error during rating creation: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the rating"
            )

    @staticmethod
    async def _validate_rating(db: Session, rating_data: CreateRatingDTO):
        """Validate rating data"""
        # Check if salon exists
        salon = db.query(Salon).filter_by(id=rating_data.salon_id).first()
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found"
            )

        # Check if user has already rated this salon
        existing_rating = db.query(Rating).filter_by(
            client_id=rating_data.client_id,
            salon_id=rating_data.salon_id
        ).first()
        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has already rated this salon"
            )

    @staticmethod
    async def _save_rating(db: Session, rating_data: CreateRatingDTO) -> Rating:
        """Save rating to database"""
        rating = Rating(**rating_data.model_dump())
        db.add(rating)
        db.commit()
        db.refresh(rating)
        
        logger.info(f"New rating created for salon {rating.salon_id}")
        return rating
