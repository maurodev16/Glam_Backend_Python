# app/services/user/__init__.py
from .get_service import ReadUserService
from .update_service import UpdateUserService
from .delete_service import DeleteUserService
from .validation_service import UserValidationService

class UserService:
    get = ReadUserService.get
    update = UpdateUserService.update
    delete = DeleteUserService.delete

__all__ = ['UserService']
