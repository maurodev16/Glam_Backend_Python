# app/services/business_hours/__init__.py
from .create_day_service import CreateDayOfWeekService

class BusinessDayService:
    create = CreateDayOfWeekService.execute


__all__ = ['BusinessHoursService']
