from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.dtos.auth.requests import RegisterUserDTO
from app.dtos.auth.responses import AuthUserResponseDTO
from app.services.auth import AuthService


logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/register", 
    response_model=AuthUserResponseDTO,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user: RegisterUserDTO,
    tenant_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> AuthUserResponseDTO:
    """Register a new user"""
    try:
        return await AuthService.register(db, user, tenant_id)
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise