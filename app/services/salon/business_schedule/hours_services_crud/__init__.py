# app/services/business_hours/__init__.py
from .create_hours_service import CreateBusinessHoursService
from .get_hours_service import GetBusinessHoursService
from .update_hours_service import UpdateBusinessHoursService
from .delete_hours_service import DeleteBusinessHoursService


class BusinessHoursService:
    create = CreateBusinessHoursService.execute
    get = GetBusinessHoursService.get_by_id
    get_all = GetBusinessHoursService.get_all
    update = UpdateBusinessHoursService.execute
    delete = DeleteBusinessHoursService.execute

__all__ = ['BusinessHoursService']
