from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.permissions.decorators.decorators import require_salon_owner
from app.models.user_model import User
from app.dtos.offering_services.responses import ServiceOfferingResponseDTO
from app.dtos.offering_services.requests import CreateOfferingServiceDTO, UpdateOfferingServiceDTO
from app.services.salon.offering_service import (
    CreateOfferingService,
    UpdateOfferingSalonService,
    DeleteOfferingSalonService,
    ListOfferingSalonService,
    GetOfferingSalonService
)

router = APIRouter()

@router.post(
    "/",
    response_model=ServiceOfferingResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_service(
    salon_id: int,
    service_data: CreateOfferingServiceDTO,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
):
    """Create a new salon service"""
    return await CreateOfferingService.execute(db=db, salon_id=salon_id, service_data=service_data, current_user=current_user)


@router.get(
    "/",
    response_model=List[ServiceOfferingResponseDTO]
)
async def list_services(
    salon_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all services for a salon"""
    return await ListOfferingSalonService.execute(
        db=db,
        skip=skip,
        limit=limit
    )

@router.get(
    "/{service_id}",
    response_model=ServiceOfferingResponseDTO
)
async def get_service(
    salon_id: int,
    service_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific service details"""
    return await GetOfferingSalonService.execute(db, service_id, salon_id)

@router.put(
    "/{service_id}",
    response_model=ServiceOfferingResponseDTO
)
async def update_service(
    salon_id: int,
    service_id: int,
    service_data: UpdateOfferingServiceDTO,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
):
    """Update a salon service"""
    return await UpdateOfferingSalonService.execute(
        db=db,
        salon_id=salon_id,
        service_id=service_id,
        service_data=service_data,
        current_user=current_user
    )

@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service(
    salon_id: int,
    service_id: int,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
):
    """Delete a salon service"""
    await DeleteOfferingSalonService.execute(
        db=db,
        salon_id=salon_id,
        current_user=current_user,
        service_id=service_id
    )
