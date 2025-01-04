# app/services/rating/__init__.py
from .create_service import CreateRatingService
from .get_service import GetRatingService
from .update_service import UpdateRatingService
from .delete_service import DeleteRatingService

class RatingService:
    create = CreateRatingService.execute
    get = GetRatingService.execute
    get_salon_ratings = GetRatingService.get_salon_ratings
    update = UpdateRatingService.execute
    delete = DeleteRatingService.execute

__all__ = ['RatingService']
