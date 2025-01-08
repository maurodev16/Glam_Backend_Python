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
from app.dtos.categories.responses import CategoryResponseDTO
from app.dtos.categories.requests import CreateCategoryDTO, UpdateCategoryDTO
from app.services.salon.category import CreateCategoryService, UpdateCategoryService, ListCategoryService, GetCategoryService, DeleteCategoryService

router = APIRouter()

@router.post(
    "/",
    response_model=CategoryResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_data: CreateCategoryDTO,
    db: Session = Depends(get_db)
):
    """Cria uma nova categoria"""
    category = CreateCategoryService.execute(db=db, category_data=category_data)
    return category

@router.put(
    "/{category_id}",
    response_model=CategoryResponseDTO
)
async def update_category(
    category_id: int,
    category_data: UpdateCategoryDTO,
    db: Session = Depends(get_db)
):
    """Atualiza uma categoria existente"""
    category = UpdateCategoryService.execute(db=db, category_id=category_id, category_data=category_data)
    return category

@router.get(
    "/{category_id}",
    response_model=CategoryResponseDTO
)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Obtém uma categoria pelo ID"""
    category = GetCategoryService.execute(db=db, category_id=category_id)
    return category

@router.get(
    "/",
    response_model=List[CategoryResponseDTO]
)
async def get_categories(db: Session = Depends(get_db)):
    """Obtém todas as categorias"""
    categories = ListCategoryService.execute(db=db)
    return categories

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Deleta uma categoria"""
    DeleteCategoryService.execute(db=db, category_id=category_id)
    return {"detail": "Category deleted successfully"}
