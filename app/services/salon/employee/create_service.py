# app/services/employee/create_employee.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.models.salon_model import Salon
from app.models.commission_model import Commission
from app.dtos.employee.requests import CreateEmployeeDTO
from app.core.security import get_password_hash
from app.core.enums.enums import UserRole, StatusRole
from .validators import validate_salon_owner, validate_new_employee

class CreateEmployeeService:
    @staticmethod
    async def execute(
        db: Session,
        salon_id: int,
        employee_data: CreateEmployeeDTO,
        current_user: User
    ) -> User:
        """Create a new employee"""
        try:
            # Validate salon owner
            await validate_salon_owner(db, salon_id, current_user.id)
            
            # Validate new employee data
            await validate_new_employee(db, employee_data)
            
            # Create new employee
            employee = User(
                name=employee_data.name,
                email=employee_data.email,
                phone=employee_data.phone,
                password=get_password_hash(employee_data.password),
                role=UserRole.EMPLOYEE,
                is_active=StatusRole.ACTIVE,
                tenant_id=current_user.tenant_id,
                bio=employee_data.bio,
                profile_image=employee_data.profile_image,
                commission_rate=employee_data.commission.value
            )
            
            db.add(employee)
            db.flush()  # Get employee ID
            
            # Create commission record
            commission = Commission(
                employee_id=employee.id,
                salon_id=salon_id,
                commission_type=employee_data.commission.commission_type,
                value=employee_data.commission.value
            )
            db.add(commission)
            
            # Get salon and add employee
            salon = db.query(Salon).filter(Salon.id == salon_id).first()
            salon.employees.append(employee)
            
            db.commit()
            db.refresh(employee)
            
            return employee
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
