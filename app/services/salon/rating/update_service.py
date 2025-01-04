# app/services/rating/update_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.rating_model import Rating
from app.dtos.rating.requests import UpdateRatingDTO
from .get_service import GetRatingService

class UpdateRatingService:
    @staticmethod
    async def execute(
        db: Session,
        rating_id: int,
        user_id: int,
        rating_data: UpdateRatingDTO
    ) -> Rating:
        try:
            rating = await GetRatingService.execute(db, rating_id)
            
            if rating.client_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this rating"
                )

            return await UpdateRatingService._update_rating(
                db, rating, rating_data
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def _update_rating(
        db: Session,
        rating: Rating,
        rating_data: UpdateRatingDTO
    ) -> Rating:
        for field, value in rating_data.model_dump(exclude_unset=True).items():
            setattr(rating, field, value)
            
        db.commit()
        db.refresh(rating)
        return rating
