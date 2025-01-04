# app/routers/users/routes/crud.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.permissions.decorators.user_decorators import require_admin, require_user_access
from app.dtos.user.responses import UserResponseDTO
from app.services.user import DeleteUserService, UserService, UpdateUserService, ReadUserService
from app.dtos.user.requests import UpdateUserDTO


router = APIRouter()

@router.get(
    "/",
    response_model=List[UserResponseDTO],
    dependencies=[Depends(require_admin())]
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
)-> List[UserResponseDTO]:
    """List all users (admin only)"""
    return await UserService.get(db, skip, limit)

@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_user_access)
)-> UserResponseDTO:
    """Get user details"""
    return await ReadUserService.get(db, user_id)

@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: int,
    user_data: UpdateUserDTO,
    db: Session = Depends(get_db),
    _: None = Depends(require_user_access)
)-> UserResponseDTO:
    """Update user details"""
    return await UpdateUserService.update(db, user_id, user_data)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin())]
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    await DeleteUserService.delete(db, user_id)
