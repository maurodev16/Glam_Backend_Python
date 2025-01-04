# app/services/employee/validators.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee_model import Employee

async def validate_employee_email(
    db: Session,
    email: str,
    employee_id: int = None
) -> None:
    """Validate employee email uniqueness"""
    query = db.query(Employee).filter(Employee.email == email)
    if employee_id:
        query = query.filter(Employee.id != employee_id)
        
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
