# app/services/employee/__init__.py
from .create_service import CreateEmployeeService
from .update_service import UpdateEmployeeService
from .get_service import GetEmployeeService
from .delete_service import DeleteEmployeeService
from .service_assignment_service import EmployeeServiceAssignmentService

class EmployeeService:
    create = CreateEmployeeService.execute
    update = UpdateEmployeeService.execute
    get = GetEmployeeService.execute
    get_all = GetEmployeeService.get_all
    delete = DeleteEmployeeService.execute
    assign_service = EmployeeServiceAssignmentService.assign
    remove_service = EmployeeServiceAssignmentService.remove

__all__ = ['EmployeeService']
