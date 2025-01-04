# app/services/employee/get_service.py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee_model import Employee

class GetEmployeeService:
    @staticmethod
    async def execute(db: Session, employee_id: int) -> Employee:
        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        return employee

    @staticmethod
    async def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Employee]:
        return db.query(Employee)\
            .offset(skip)\
            .limit(limit)\
            .all()
