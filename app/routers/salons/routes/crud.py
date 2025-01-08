# app/routers/salons/routes/crud.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.permissions.decorators.decorators import require_salon_owner
from app.models.user_model import User
from app.dtos.salon.requests import CreateSalonDTO, UpdateSalonDTO
from app.dtos.salon.responses import SalonResponseDTO, SalonListResponseDTO
from app.services.salon.salon_management import (
    CreateSalonServiceCrud,
    GetSalonServiceCrud,
    ListSalonServiceCrud,
    DeleteSalonServiceCrud,
    ListOwnerSalonsServiceCrud,
    UpdateSalonServiceCrud
)
from app.routers.auth.dependencies.dependecies import (
    get_current_user_optional,
    get_current_user
)

router = APIRouter()

@router.post(
    "/",
    response_model=SalonResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Salon created successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Authentication required when using existing user"},
        500: {"description": "Internal server error"}
    }
)
async def create_salon(
    salon_data: CreateSalonDTO,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
) -> SalonResponseDTO:
    """Create a new salon"""
    try:
        return await CreateSalonServiceCrud.execute(db, salon_data, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[SalonListResponseDTO],
    responses={
        200: {"description": "List of salons retrieved successfully"},
        500: {"description": "Internal server error"}
    }
)
async def list_salons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[SalonListResponseDTO]:
    """List all public salons"""
    try:
        return await ListSalonServiceCrud.execute(db, skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/my",
    response_model=List[SalonResponseDTO],
    responses={
        200: {"description": "List of owned salons retrieved successfully"},
        401: {"description": "User not authenticated"},
        500: {"description": "Internal server error"}
    }
)
async def get_my_salons(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[SalonResponseDTO]:
    """Get salons owned by current user"""
    try:
        return await ListOwnerSalonsServiceCrud.execute(db, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/{salon_id}",
    response_model=SalonResponseDTO,
    responses={
        200: {"description": "Salon details retrieved successfully"},
        404: {"description": "Salon not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_salon(
    salon_id: int,
    db: Session = Depends(get_db)
) -> SalonResponseDTO:
    """Get salon details by ID"""
    try:
        salon = await GetSalonServiceCrud.execute(db, salon_id)
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found"
            )
        return salon
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put(
    "/{salon_id}",
    response_model=SalonResponseDTO,
    responses={
        200: {"description": "Salon updated successfully"},
        403: {"description": "Not authorized to update this salon"},
        404: {"description": "Salon not found"},
        500: {"description": "Internal server error"}
    }
)
async def update_salon(
    salon_id: int,
    salon_data: UpdateSalonDTO,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
) -> SalonResponseDTO:
    """Update salon information"""
    try:
        return await UpdateSalonServiceCrud.execute(db, salon_id, salon_data, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{salon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Salon deleted successfully"},
        403: {"description": "Not authorized to delete this salon"},
        404: {"description": "Salon not found"},
        500: {"description": "Internal server error"}
    }
)
async def delete_salon(
    salon_id: int,
    current_user: User = Depends(require_salon_owner),
    db: Session = Depends(get_db)
):
    """Delete salon"""
    try:
        await DeleteSalonServiceCrud.execute(db, salon_id, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
