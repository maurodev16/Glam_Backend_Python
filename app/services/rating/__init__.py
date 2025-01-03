# app/services/rating/__init__.py
from .create_rating_service import CreateRatingService
from .update_rating_service import UpdateRatingService

class RatingService:
    create = CreateRatingService.create_rating
    update = UpdateRatingService.update_rating

__all__ = ['RatingService']
