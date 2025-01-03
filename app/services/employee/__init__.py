# app/services/employee/__init__.py
from .create_employee_service import CreateEmployeeService

class EmployeeService:
    create = CreateEmployeeService.create_employee
    #update = UpdateRatingService.update_rating

__all__ = ['EmployeeService']
