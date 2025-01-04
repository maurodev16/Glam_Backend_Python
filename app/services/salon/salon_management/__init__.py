# app/services/salon/service_management/__init__.py
from .create_service_crud import CreateServiceService
from .list_service_crud import ListServiceService
from .get_service_crud import GetServiceService
from .update_service_crud import UpdateServiceService
from .delete_service_crud import DeleteServiceService
from .list_owner_salons_service_crud import ListOwnerSalonsService

class SalonServiceManagement:
    create = CreateServiceService.execute
    list_by_salon = ListServiceService.execute
    get_owner_salons = ListOwnerSalonsService.execute
    get = GetServiceService.execute
    update = UpdateServiceService.execute
    delete = DeleteServiceService.execute

__all__ = ['SalonServiceManagement']
