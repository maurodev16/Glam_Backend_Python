from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.user_model import User
from app.routers.auth.dependencies.dependecies import get_current_user
from app.services.salon.business_schedule.hours_services_crud import (BusinessHoursService)
from app.dtos.business_schedule.business_hours.responses import CreatedBusinessHoursResponseDTO
from app.dtos.business_schedule.business_hours.requests import CreateBusinessHoursRequestDTO, UpdateBusinessHoursRequetsDTO

router = APIRouter()

@router.post("/", response_model=CreatedBusinessHoursResponseDTO)
async def create_business_hours(
    salon_id: int,
    hours_data: CreateBusinessHoursRequestDTO,
    get_current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await BusinessHoursService.create(salon_id=salon_id,current_user=get_current_user, hours_data=hours_data, db=db)


@router.get("/", response_model=List[CreatedBusinessHoursResponseDTO])
async def get_business_hours(
    salon_id: int,
    day_of_week: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get business hours for all days or specific day"""
    return await BusinessHoursService.get_all(
        db=db,
        salon_id=salon_id,
        day_of_week=day_of_week
    )


@router.put("/{day_of_week}", response_model=CreatedBusinessHoursResponseDTO)
async def update_business_hours(
    salon_id: int,
    day_of_week: int,
    hours_data: UpdateBusinessHoursRequetsDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update business hours for a specific day"""
    return await BusinessHoursService.update(
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
    await BusinessHoursService.update(
        db=db,
        salon_id=salon_id,
        user_id=current_user.id,
        day_of_week=day_of_week
    )
