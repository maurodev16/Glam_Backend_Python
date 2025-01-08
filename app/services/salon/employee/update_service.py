# app/services/employee/update_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.models.commission_model import Commission
from app.dtos.employee.requests import UpdateEmployeeDTO
from .validators import validate_salon_owner
from .get_service import GetEmployeeService

class UpdateEmployeeService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        employee_id: int,
        employee_data: UpdateEmployeeDTO,
        current_user: User
    ) -> User:
        """Update employee information"""
        try:
            # Validate salon owner
            await validate_salon_owner(db, salon_id, current_user.id)
            
            # Get employee
            employee = await GetEmployeeService.execute(db, salon_id, employee_id)
            
            # Update employee and commission
            return await UpdateEmployeeService._update_employee(
                db, employee, salon_id, employee_data
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
        employee: User,
        salon_id: int,
        employee_data: UpdateEmployeeDTO
    ) -> User:
        """Apply updates to employee"""
        # Update basic employee fields
        update_data = employee_data.model_dump(
            exclude={'commission'}, 
            exclude_unset=True
        )
        for field, value in update_data.items():
            setattr(employee, field, value)
            
        # Update commission if provided
        if employee_data.commission:
            commission = db.query(Commission).filter(
                Commission.employee_id == employee.id,
                Commission.salon_id == salon_id
            ).first()
            
            if commission:
                commission.commission_type = employee_data.commission.commission_type
                commission.value = employee_data.commission.value
            
        db.commit()
        db.refresh(employee)
        return employee
