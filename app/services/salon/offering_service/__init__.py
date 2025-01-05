# app/services/salon/__init__.py
from .create_offering_service import CreateOfferingService
from .list_offering_salon import ListOfferingSalonService
from .get_offering_salon import GetOfferingSalonService
from .update_offering_salon import UpdateOfferingSalonService
from .delete_offering_salon import DeleteOfferingSalonService

class SalonOfferingService:
    create = CreateOfferingService.execute
    list = ListOfferingSalonService.execute
    get = GetOfferingSalonService.execute
    update = UpdateOfferingSalonService.execute
    delete = DeleteOfferingSalonService.execute

__all__ = ['SalonService']
