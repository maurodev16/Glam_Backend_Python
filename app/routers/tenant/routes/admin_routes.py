from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user_model import User
from app.core.enums.enums import UserRole
from app.services.tenant import TenantService
from app.dtos.tenant.responses import TenantResponseDTO
from app.routers.auth.dependencies.dependecies import get_current_user

router = APIRouter()

async def verify_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/", response_model=List[TenantResponseDTO])
async def list_all_tenants(
    db: Session = Depends(get_db),
    _: User = Depends(verify_admin)
) -> List[TenantResponseDTO]:
    """List all tenants (admin only)"""
    return await TenantService.list_tenants(db)

@router.get("/active", response_model=List[TenantResponseDTO])
async def list_active_tenants(
    db: Session = Depends(get_db),
    _: User = Depends(verify_admin)
) -> List[TenantResponseDTO]:
    """List active tenants (admin only)"""
    return await TenantService.list_active_tenants(db)