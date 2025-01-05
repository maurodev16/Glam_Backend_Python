# backend/app/routers/auth/routes/me.py
from multiprocessing import AuthenticationError
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dtos.user.requests import UpdatePasswordDTO, UpdateUserDTO
from app.dtos.user.responses import UserResponseDTO
from app.services.user import UserService
from ..dependencies.dependecies import get_current_user
from ....models import user_model as models
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/me", response_model=UserResponseDTO)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=UserResponseDTO)
async def update_user(
    user_data: UpdateUserDTO,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        logger.debug(f"Updating user {current_user.id}")
        updated_user = await UserService.update_user(db, current_user.id, user_data)
        logger.debug("User updated successfully")
        return updated_user
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise AuthenticationError("Failed to update user")

@router.put("/me/password")
async def update_password(
    password_data: UpdatePasswordDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    await UserService.update_password(
        db, 
        current_user.id, 
        password_data.current_password,
        password_data.new_password
    )
    return {"message": "Password updated successfully"}
