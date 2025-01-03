# app/services/employee/create_employee_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.employee_model import Employee
from app.dtos.employee.requests import CreateEmployeeDTO
from app.models.employee_service_model import EmployeeService

logger = logging.getLogger(__name__)

class CreateEmployeeService:
    @staticmethod
    async def create_employee(
        db: Session,
        employee_data: CreateEmployeeDTO
    ) -> Employee:
        try:
            await CreateEmployeeService._validate_employee(db, employee_data)
            return await CreateEmployeeService._save_employee(db, employee_data)
        except SQLAlchemyError as e:
            logger.error(f"Database error creating employee: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating employee"
            )

    @staticmethod
    async def _validate_employee(db: Session, employee_data: CreateEmployeeDTO):
        if employee_data.email:
            existing = db.query(Employee).filter_by(email=employee_data.email).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

    @staticmethod
    async def _save_employee(db: Session, employee_data: CreateEmployeeDTO) -> Employee:
        employee = Employee(**employee_data.model_dump(exclude={'service_ids'}))
        db.add(employee)
        db.flush()

        # Add employee services
        for service_id in employee_data.service_ids:
            employee_service = EmployeeService(
                employee_id=employee.id,
                service_id=service_id
            )
            db.add(employee_service)

        db.commit()
        db.refresh(employee)
        return employee
