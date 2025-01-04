# app/services/employee/service_assignment_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee_service_model import EmployeeService
from .get_service import GetEmployeeService

class EmployeeServiceAssignmentService:
    @staticmethod
    async def assign(
        db: Session,
        employee_id: int,
        service_id: int
    ) -> None:
        await GetEmployeeService.execute(db, employee_id)
        
        if db.query(EmployeeService).filter_by(
            employee_id=employee_id,
            service_id=service_id
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service already assigned to employee"
            )

        db.add(EmployeeService(
            employee_id=employee_id,
            service_id=service_id
        ))
        db.commit()

    @staticmethod
    async def remove(
        db: Session,
        employee_id: int,
        service_id: int
    ) -> None:
        await GetEmployeeService.execute(db, employee_id)
        
        assignment = db.query(EmployeeService).filter_by(
            employee_id=employee_id,
            service_id=service_id
        ).first()
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not assigned to employee"
            )

        db.delete(assignment)
        db.commit()
