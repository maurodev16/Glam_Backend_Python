# app/routers/salons/routes/employees.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.permissions.decorators.decorators import require_salon_owner
from app.services.salon.employee import EmployeeService
from app.dtos.employee.responses import EmployeeResponseDTO
from app.dtos.employee.requests import CreateEmployeeDTO, UpdateEmployeeDTO
from app.models.user_model import User
from app.routers.auth.dependencies.dependecies import get_current_user

router = APIRouter()

@router.post("/", response_model=EmployeeResponseDTO)
async def create_employee(
    salon_id: int,
    employee: CreateEmployeeDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new employee for a salon"""
    return await EmployeeService.create(db, salon_id, employee, current_user)

@router.get("/", response_model=List[EmployeeResponseDTO])
async def list_employees(
    salon_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all employees for a salon"""
    return await EmployeeService.list_by_salon(db, salon_id, skip, limit)

@router.get("/{employee_id}", response_model=EmployeeResponseDTO)
async def get_employee(
    salon_id: int,
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific employee by ID"""
    return await EmployeeService.get(db, salon_id, employee_id)

@router.put("/{employee_id}", response_model=EmployeeResponseDTO)
async def update_employee(
    salon_id: int,
    employee_id: int,
    employee: UpdateEmployeeDTO,
    db: Session = Depends(get_db)
):
    """Update an employee's information"""
    return await EmployeeService.update(db, salon_id, employee_id, employee)

@router.delete("/{employee_id}")
async def delete_employee(
    salon_id: int,
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Delete an employee"""
    await EmployeeService.delete(db, salon_id, employee_id)
    return {"message": "Employee deleted successfully"}
