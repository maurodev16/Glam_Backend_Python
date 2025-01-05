# app/services/salon/service_management/__init__.py
from .create_salao_crud import CreateSalonServiceCrud
from .list_salons_crud import ListSalonServiceCrud
from .get_salon_crud import GetSalonServiceCrud
from .update_salon_crud import UpdateSalonServiceCrud
from .delete_salon_crud import DeleteSalonServiceCrud
from .list_owner_salons_crud import ListOwnerSalonsServiceCrud

class SalonServiceManagement:
    create = CreateSalonServiceCrud.execute
    list_by_salon = ListSalonServiceCrud.execute
    get_owner_salons = ListOwnerSalonsServiceCrud.execute
    get = GetSalonServiceCrud.execute
    update = UpdateSalonServiceCrud.execute
    delete = DeleteSalonServiceCrud.execute

__all__ = ['SalonServiceManagement']
