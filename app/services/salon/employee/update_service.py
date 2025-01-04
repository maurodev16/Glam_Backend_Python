# app/services/employee/update_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee_model import Employee
from app.dtos.employee.requests import UpdateEmployeeDTO
from .validators import validate_employee_email
from .get_service import GetEmployeeService

class UpdateEmployeeService:
    @staticmethod
    async def execute(
        db: Session,
        employee_id: int,
        employee_data: UpdateEmployeeDTO
    ) -> Employee:
        try:
            employee = await GetEmployeeService.execute(db, employee_id)
            if employee_data.email:
                await validate_employee_email(db, employee_data.email, employee_id)
            return await UpdateEmployeeService._update_employee(
                db, employee, employee_data
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def _update_employee(
        db: Session,
        employee: Employee,
        employee_data: UpdateEmployeeDTO
    ) -> Employee:
        for field, value in employee_data.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)
            
        db.commit()
        db.refresh(employee)
        return employee
