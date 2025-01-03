# app/services/rating/update_rating_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.rating_model import Rating
from dtos.rating.requests import UpdateRatingDTO

logger = logging.getLogger(__name__)

class UpdateRatingService:
    @staticmethod
    async def update_rating(
        db: Session,
        rating_id: int,
        client_id: int,
        rating_data: UpdateRatingDTO
    ) -> Rating:
        """Update an existing rating"""
        try:
            rating = await UpdateRatingService._get_rating(db, rating_id, client_id)
            return await UpdateRatingService._save_updates(db, rating, rating_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error during rating update: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the rating"
            )

    @staticmethod
    async def _get_rating(db: Session, rating_id: int, client_id: int) -> Rating:
        """Get rating and verify ownership"""
        rating = db.query(Rating).filter_by(id=rating_id).first()
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rating not found"
            )
        if rating.client_id != client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this rating"
            )
        return rating

    @staticmethod
    async def _save_updates(
        db: Session,
        rating: Rating,
        rating_data: UpdateRatingDTO
    ) -> Rating:
        """Apply and save rating updates"""
        for field, value in rating_data.model_dump(exclude_unset=True).items():
            setattr(rating, field, value)
            
        db.commit()
        db.refresh(rating)
        
        logger.info(f"Rating {rating.id} updated")
        return rating
