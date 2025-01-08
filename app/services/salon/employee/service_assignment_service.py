# app/services/employee/service_assignment_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.offering_services_model import OfferingService
from .validators import validate_salon_owner, validate_services_exist

class EmployeeServiceAssignmentService:
    @staticmethod
    async def assign(
        db: Session,
        salon_id: int,
        employee_id: int,
        service_id: int,
        current_user_id: int
    ) -> None:
        """Assign a service to an employee"""
        # Validate salon owner
        salon = await validate_salon_owner(db, salon_id, current_user_id)
        
        # Validate service exists in salon
        await validate_services_exist(db, [service_id], salon_id)
        
        # Check if already assigned
        if db.query(OfferingService).filter_by(
            employee_id=employee_id,
            service_id=service_id
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service already assigned to employee"
            )

        # Create assignment
        assignment = OfferingService(
            employee_id=employee_id,
            service_id=service_id
        )
        db.add(assignment)
        db.commit()

    @staticmethod
    async def remove(
        db: Session,
        salon_id: int,
        employee_id: int,
        service_id: int,
        current_user_id: int
    ) -> None:
        """Remove a service assignment from an employee"""
        # Validate salon owner
        await validate_salon_owner(db, salon_id, current_user_id)
        
        # Find and remove assignment
        assignment = db.query(OfferingService).filter_by(
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
