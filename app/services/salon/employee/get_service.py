# app/services/employee/get_service.py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.models.salon_model import Salon

class GetEmployeeService:
    @staticmethod
    async def execute(db: Session, salon_id: int, employee_id: int) -> User:
        """Get employee by ID for a specific salon"""
        salon = db.query(Salon).filter(Salon.id == salon_id).first()
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found"
            )
            
        employee = db.query(User)\
            .join(Salon.employees)\
            .filter(User.id == employee_id)\
            .filter(Salon.id == salon_id)\
            .first()
            
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found in this salon"
            )
        return employee

    @staticmethod
    async def get_all(db: Session, salon_id: int) -> List[User]:
        """Get all employees for a salon"""
        salon = db.query(Salon).filter(Salon.id == salon_id).first()
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found"
            )
        return salon.employees
