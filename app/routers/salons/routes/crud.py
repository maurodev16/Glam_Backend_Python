# app/routers/salons/routes/crud.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.permissions.decorators.decorators import require_salon_owner
from app.models.user_model import User
from app.models.salon_model import Salon
from app.dtos.salon.requests import CreateSalonDTO, UpdateSalonDTO
from app.dtos.salon.responses import SalonResponseDTO, SalonListResponseDTO
from app.services.salon.salon_management.create_service_crud import CreateServiceService
from app.services.salon.salon_management.get_service_crud import GetServiceService
from app.services.salon.salon_management.list_service_crud import ListServiceService
from app.services.salon.salon_management.delete_service_crud import DeleteServiceService
from app.services.salon.salon_management.list_owner_salons_service_crud import ListOwnerSalonsService
from app.routers.auth.dependencies import get_current_user
from app.services.salon.salon_service import SalonService

router = APIRouter()

@router.post("/", response_model=SalonResponseDTO)
async def create_salon(
    salon_data: CreateSalonDTO,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new salon"""
    return await CreateServiceService.execute (db, salon_data, current_user)

@router.get("/", response_model=List[SalonListResponseDTO])
async def list_salons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all public salons"""
    return await ListServiceService.execute(db, skip, limit)

@router.get("/{salon_id}", response_model=SalonResponseDTO)
async def get_salon(
    salon_id: int,
    db: Session = Depends(get_db)
):
    """Get salon details"""
    salon = await GetServiceService.execute(db, salon_id)
    if not salon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salon not found"
        )
    return salon

@router.put("/{salon_id}", response_model=SalonResponseDTO)
async def update_salon(
    salon_id: int,
    salon_data: UpdateSalonDTO,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
) -> SalonResponseDTO:
    """Update salon information"""
    return await SalonService.update(db, salon_id, salon_data, current_user)

@router.delete("/{salon_id}")
async def delete_salon(
    salon_id: int,
    current_user: User = Depends(require_salon_owner),
    #service_id: int,
    db: Session = Depends(get_db),
    
):
    """Delete salon (salon owner only)"""
    await DeleteServiceService.execute(db, salon_id, current_user)
    return {"message": "Salon deleted successfully"}

@router.get("/my-salons", response_model=List[SalonResponseDTO])
async def get_my_salons(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get salons owned by current user"""
    return await ListOwnerSalonsService.execute(db, current_user)
