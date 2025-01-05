# app/services/rating/validators.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.rating_model import Rating
from app.models.salon_model import Salon
from app.dtos.rating.requests import CreateRatingDTO

async def validate_rating_data(db: Session, rating_data: CreateRatingDTO) -> None:
    """Validate rating data before creation"""
    # Check if salon exists
    salon = db.query(Salon).filter_by(id=rating_data.salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salon not found"
        )

    # Check for duplicate rating
    existing_rating = db.query(Rating).filter_by(
        user_id=rating_data.user_id,
        salon_id=rating_data.salon_id
    ).first()
    
    if existing_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has already rated this salon"
        )

    # Validate rating value
    if not 1 <= rating_data.rating <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
