# backend/app/routers/users/routes/crud.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dtos.user import responses
from app.core.enums.enums import UserRole
from app.core.permissions import check_permissions
from ....core.database import get_db
from ....models import user_model as models
from ...auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[responses.UserResponseDTO])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List users (admin only)"""
    if not check_permissions(current_user, [UserRole.ADMIN]):
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(models.User).offset(skip).limit(limit).all()

@router.get("/{user_id}", response_model=responses.UserResponseDTO)
async def get_user(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user details"""
    if not check_permissions(current_user, [UserRole.ADMIN]) and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    if not check_permissions(current_user, [UserRole.ADMIN]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
