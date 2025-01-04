# app/routers/salons/routes/services.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.permissions.decorators.decorators import require_salon_owner
from app.models.user_model import User
from app.dtos.salon_services.responses import ServiceResponseDTO
from app.dtos.salon_services.requests import CreateServiceDTO, UpdateServiceDTO
from app.routers.auth.dependencies import get_current_user
from app.services.salon.salon_service import create_service, list_salon, delete_salon, update_salon, get_salon

router = APIRouter()

@router.post("/{salon_id}/services", 
    response_model=ServiceResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_service(
    salon_id: int,
    service_data: CreateServiceDTO,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
):
    """Create a new salon service"""
    return await create_service (
        db, 
        salon_id, 
        service_data
    )

@router.get("/{salon_id}/services",
    response_model=List[ServiceResponseDTO]
)
async def list_services(
    salon_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all services for a salon"""
    return await list_salon(
        db,
        salon_id,
        skip,
        limit
    )

@router.get("/{salon_id}/services/{service_id}",
    response_model=ServiceResponseDTO
)
async def get_service(
    salon_id: int,
    service_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific service details"""
    service = await get_salon(db, salon_id, service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return service

@router.put("/{salon_id}/services/{service_id}",
    response_model=ServiceResponseDTO
)
async def update_service(
    salon_id: int,
    service_id: int,
    service_data: UpdateServiceDTO,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
):
    """Update a salon service"""
    return await update_salon(
        db,
        salon_id,
        service_id,
        service_data
    )

@router.delete("/{salon_id}/services/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service(
    salon_id: int,
    service_id: int,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
):
    """Delete a salon service"""
    await delete_salon(db, salon_id, service_id)
