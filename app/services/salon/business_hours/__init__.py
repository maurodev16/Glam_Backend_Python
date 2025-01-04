# app/services/business_hours/__init__.py
from .create_service import CreateBusinessHoursService
from .update_service import UpdateBusinessHoursService
from .get_service import GetBusinessHoursService
from .delete_service import DeleteBusinessHoursService

class BusinessHoursService:
    create = CreateBusinessHoursService.execute
    update = UpdateBusinessHoursService.execute
    get = GetBusinessHoursService.execute
    delete = DeleteBusinessHoursService.execute

__all__ = ['BusinessHoursService']
