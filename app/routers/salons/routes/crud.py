# app/routers/salons/routes/crud.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.permissions.decorators.decorators import require_salon_owner
from app.models.user_model import User
from app.models.salon_model import Salon
from app.dtos.salon.requests import CreateSalonDTO, UpdateSalonDTO
from app.dtos.salon.responses import SalonResponseDTO, SalonListResponseDTO
from app.services.salon.salon_management.create_salao_crud import CreateSalonServiceCrud
from app.services.salon.salon_management.get_salon_crud import GetSalonServiceCrud
from app.services.salon.salon_management.list_salons_crud import ListSalonServiceCrud
from app.services.salon.salon_management.delete_salon_crud import DeleteSalonServiceCrud
from app.services.salon.salon_management.list_owner_salons_crud import ListOwnerSalonsServiceCrud
from app.services.salon.salon_management.update_salon_crud import UpdateSalonServiceCrud
from app.routers.auth.dependencies.dependecies import get_current_user_optional
from app.routers.auth.dependencies.dependecies import get_current_user

router = APIRouter()

@router.post("/", response_model=SalonResponseDTO,status_code=status.HTTP_201_CREATED,    responses={
        201: {
            "description": "Salon created successfully",
            "model": SalonResponseDTO
        },
        400: {
            "description": "Invalid input data"
        },
        401: {
            "description": "Authentication required when using existing user"
        },
        500: {
            "description": "Internal server error"
        }
    }
)
async def create_salon(
    salon_data: CreateSalonDTO,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
) -> SalonResponseDTO:
    """
    Create a new salon with flexible user handling.
    
    This endpoint supports two scenarios:
    1. Creating a salon with a new user account
    2. Creating a salon using an existing user account
    
    When using an existing account (use_existing_user=True):
    - User must be authenticated
    - Owner information is not required
    
    When creating a new account (use_existing_user=False):
    - Authentication is optional
    - All owner information fields are required
    """
    return await CreateSalonServiceCrud.execute(db, salon_data, current_user)


@router.get("/", response_model=List[SalonListResponseDTO])
async def list_salons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all public salons"""
    return await ListSalonServiceCrud.execute(db, skip, limit)

@router.get("/{salon_id}", response_model=SalonResponseDTO)
async def get_salon(
    salon_id: int,
    db: Session = Depends(get_db)
):
    """Get salon details"""
    salon = await GetSalonServiceCrud.execute(db, salon_id)
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
    return await UpdateSalonServiceCrud.execute(db, salon_id, salon_data, current_user)

@router.delete("/{salon_id}")
async def delete_salon(
    salon_id: int,
    current_user: User = Depends(require_salon_owner),
    #service_id: int,
    db: Session = Depends(get_db),
    
):
    """Delete salon (salon owner only)"""
    await DeleteSalonServiceCrud.execute(db, salon_id, current_user)
    return {"message": "Salon deleted successfully"}

@router.get("/my-salons", response_model=List[SalonResponseDTO])
async def get_my_salons(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get salons owned by current user"""
    return await ListOwnerSalonsServiceCrud.execute(db, current_user)
