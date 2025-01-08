from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.models.salon_model import Salon
from app.models.offering_services_model import OfferingService
from .validators import validate_salon_owner
from .get_service import GetEmployeeService

class DeleteEmployeeService:
    @staticmethod
    async def execute(
        db: Session, 
        salon_id: int,
        employee_id: int,
        current_user: User
    ) -> None:
        """Remove employee from salon"""
        try:
            # Validate salon owner
            await validate_salon_owner(db, salon_id, current_user.id)
            
            # Get employee
            employee = await GetEmployeeService.execute(db, salon_id, employee_id)
            
            # Delete employee services first
            db.query(OfferingService).filter(
                OfferingService.employee_id == employee_id
            ).delete()
            
            # Remove employee from salon
            salon = db.query(Salon).filter(Salon.id == salon_id).first()
            salon.employees.remove(employee)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
