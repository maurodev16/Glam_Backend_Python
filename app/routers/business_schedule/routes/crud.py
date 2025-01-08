from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.user_model import User
from app.dtos.business_hours.responses import BusinessHoursResponseDTO
from app.dtos.business_hours.requests import CreateBusinessHoursDTO, UpdateBusinessHoursDTO
from app.routers.auth.dependencies.dependecies import get_current_user
from app.services.salon.business_schedule import (
    CreateBusinessHoursService,
    GetBusinessHoursService,
    UpdateBusinessHoursService,
    DeleteBusinessHoursService
)
router = APIRouter()

@router.post("/", response_model=List[BusinessHoursResponseDTO])
async def create_business_hours(
    salon_id: int,
    hours_data: List[CreateBusinessHoursDTO],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create business hours for multiple days"""
    return await CreateBusinessHoursService.execute(
        db=db,
        salon_id=salon_id,
        hours_data=hours_data,
        user_id=current_user.id
    )

@router.get("/", response_model=List[BusinessHoursResponseDTO])
async def get_business_hours(
    salon_id: int,
    day_of_week: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get business hours for all days or specific day"""
    return await GetBusinessHoursService.get_all(
        db=db,
        salon_id=salon_id,
        day_of_week=day_of_week
    )

@router.put("/{day_of_week}", response_model=BusinessHoursResponseDTO)
async def update_business_hours(
    salon_id: int,
    day_of_week: int,
    hours_data: UpdateBusinessHoursDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update business hours for a specific day"""
    return await UpdateBusinessHoursService.execute(
        db=db,
        salon_id=salon_id,
        user_id=current_user.id,
        day_of_week=day_of_week,
        hours_data=hours_data
    )

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business_hours(
    salon_id: int,
    day_of_week: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete all business hours or for a specific day"""
    await DeleteBusinessHoursService.execute(
        db=db,
        salon_id=salon_id,
        user_id=current_user.id,
        day_of_week=day_of_week
    )
