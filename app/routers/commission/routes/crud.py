from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user_model import User
from app.services.commission import CommissionService
from app.dtos.commission.requests import CreateCommissionDTO, UpdateCommissionDTO
from app.dtos.commission.responses import CommissionResponseDTO
from app.routers.auth.dependencies.dependecies import get_current_user
from app.core.permissions.salon_permissions import SalonPermissions

router = APIRouter()

@router.post("/", response_model=CommissionResponseDTO)
async def create_commission(
    salon_id: int,
    employee_id: int,
    commission_data: CreateCommissionDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new commission for an employee"""
    await SalonPermissions.verify_salon_owner(db, salon_id, current_user.id)
    return await CommissionService.create_commission(db, salon_id, employee_id, commission_data)

@router.get("/", response_model=CommissionResponseDTO)
async def get_employee_commission(
    salon_id: int,
    employee_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get commission for a specific employee"""
    await SalonPermissions.verify_salon_owner(db, salon_id, current_user.id)
    return await CommissionService.get_employee_commission(db, salon_id, employee_id)

@router.put("/", response_model=CommissionResponseDTO)
async def update_employee_commission(
    salon_id: int,
    employee_id: int,
    commission_data: UpdateCommissionDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update commission for an employee"""
    await SalonPermissions.verify_salon_owner(db, salon_id, current_user.id)
    return await CommissionService.update_commission(db, salon_id, employee_id, commission_data)