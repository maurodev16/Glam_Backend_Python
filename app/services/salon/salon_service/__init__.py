# app/services/salon/__init__.py
from .create_service import CreateSalonService
from .list_salon import ListSalonService
from .get_salon import GetSalonService
from .update_salon import UpdateSalonService
from .delete_salon import DeleteSalonService

class SalonService:
    create = CreateSalonService.execute
    list_salons = ListSalonService.execute
    get = GetSalonService.execute
    update = UpdateSalonService.execute
    delete = DeleteSalonService.execute

__all__ = ['SalonService']
