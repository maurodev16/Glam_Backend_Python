# app/services/employee/create_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee_model import Employee
from app.models.employee_service_model import EmployeeService
from app.dtos.employee.requests import CreateEmployeeDTO
from .validators import validate_employee_email

class CreateEmployeeService:
    @staticmethod
    async def execute(
        db: Session,
        employee_data: CreateEmployeeDTO
    ) -> Employee:
        try:
            await validate_employee_email(db, employee_data.email)
            return await CreateEmployeeService._save_employee(db, employee_data)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def _save_employee(db: Session, employee_data: CreateEmployeeDTO) -> Employee:
        employee = Employee(**employee_data.model_dump(exclude={'service_ids'}))
        db.add(employee)
        db.flush()

        for service_id in employee_data.service_ids:
            employee_service = EmployeeService(
                employee_id=employee.id,
                service_id=service_id
            )
            db.add(employee_service)

        db.commit()
        db.refresh(employee)
        return employee
