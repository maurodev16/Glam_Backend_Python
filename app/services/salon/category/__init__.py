# app/services/employee/__init__.py
from .create_service import CreateCategoryService
from .update_service import UpdateCategoryService
from .get_service import GetCategoryService
from .delete_service import DeleteCategoryService
from.list_service import ListCategoryService


class EmployeeService:
    create = CreateCategoryService.execute
    update = UpdateCategoryService.execute
    get = GetCategoryService.execute
    get_all = ListCategoryService.execute
    delete = DeleteCategoryService.execute

__all__ = ['EmployeeService']
