# app/services/rating/delete_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .get_service import GetRatingService

class DeleteRatingService:
    @staticmethod
    async def execute(db: Session, rating_id: int, user_id: int) -> None:
        rating = await GetRatingService.execute(db, rating_id)
        
        if rating.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this rating"
            )

        db.delete(rating)
        db.commit()
