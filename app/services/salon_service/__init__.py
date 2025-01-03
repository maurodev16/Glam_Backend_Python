# app/services/salon_service/__init__.py
from .create_salon_service import CreateSalonService
#from .update_rating_service import UpdateRatingService

class SalonService:
    create = CreateSalonService.create_salon_service
    #update = UpdateRatingService.update_rating

__all__ = ['SalonService']
