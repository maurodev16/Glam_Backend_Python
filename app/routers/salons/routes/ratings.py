# app/routers/salons/routes/ratings.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.permissions.decorators.decorators import require_can_rate
from app.models.user_model import User
from app.dtos.rating.requests import CreateRatingDTO
from app.dtos.rating.responses import RatingResponseDTO
from app.services.salon.rating import RatingService

router = APIRouter()

@router.post("/{salon_id}/ratings", response_model=RatingResponseDTO)
async def create_rating(
    salon_id: int,
    rating_data: CreateRatingDTO,
    current_user: User = Depends(require_can_rate),
    db: Session = Depends(get_db)
):
    """Create a new rating for a salon"""
    return await RatingService.create_rating(db, salon_id, rating_data, current_user)

@router.get("/{salon_id}/ratings", response_model=List[RatingResponseDTO])
async def list_salon_ratings(
    salon_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all ratings for a salon"""
    return await RatingService.list_salon_ratings(db, salon_id, skip, limit)
