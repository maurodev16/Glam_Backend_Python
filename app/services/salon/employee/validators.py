# app/services/employee/validators.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.salon_model import Salon
from app.models.user_model import User
from app.dtos.employee.requests import CreateEmployeeDTO
from app.models.offering_services_model import OfferingService

async def validate_salon_owner(db: Session, salon_id: int, user_id: int):
    """Validate if user is the salon owner"""
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salon not found"
        )
    if salon.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only salon owner can manage employees"
        )
    return salon

async def validate_new_employee(db: Session, employee_data: CreateEmployeeDTO):
    """Validate new employee data"""
    await validate_employee_email(db, employee_data.email)
    await validate_employee_phone(db, employee_data.phone)
    if employee_data.service_ids:
        await validate_services_exist(db, employee_data.service_ids)

async def validate_employee_email(db: Session, email: str, employee_id: int = None):
    """Validate employee email uniqueness"""
    query = db.query(User).filter(User.email == email)
    if employee_id:
        query = query.filter(User.id != employee_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

async def validate_employee_phone(db: Session, phone: str, employee_id: int = None):
    """Validate employee phone uniqueness"""
    query = db.query(User).filter(User.phone == phone)
    if employee_id:
        query = query.filter(User.id != employee_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

async def validate_services_exist(db: Session, service_ids: list[int], salon_id: int):
    """Validate that all services exist and belong to the salon"""
    for service_id in service_ids:
        service = db.query(OfferingService).filter(
            OfferingService.id == service_id,
            OfferingService.salon_id == salon_id
        ).first()
        if not service:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service {service_id} not found in this salon"
            )
