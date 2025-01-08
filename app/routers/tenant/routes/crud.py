from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.tenant import TenantService
from app.dtos.tenant.requests import CreateTenantDTO, UpdateTenantDTO
from app.dtos.tenant.responses import TenantResponseDTO
from app.routers.tenant.routes.dependencies import verify_tenant_access

router = APIRouter()

@router.post("/", response_model=TenantResponseDTO)
async def create_tenant(
    tenant_data: CreateTenantDTO,
    db: Session = Depends(get_db)
) -> TenantResponseDTO:
    """Create a new tenant"""
    return await TenantService.create_tenant(db, tenant_data)

@router.get("/{tenant_id}", response_model=TenantResponseDTO)
async def get_tenant(
    tenant: TenantResponseDTO = Depends(verify_tenant_access)
) -> TenantResponseDTO:
    """Get tenant by ID"""
    return tenant

@router.put("/{tenant_id}", response_model=TenantResponseDTO)
async def update_tenant(
    tenant_data: UpdateTenantDTO,
    tenant: TenantResponseDTO = Depends(verify_tenant_access),
    db: Session = Depends(get_db)
) -> TenantResponseDTO:
    """Update tenant information"""
    return await TenantService.update_tenant(db, tenant.id, tenant_data)

@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant: TenantResponseDTO = Depends(verify_tenant_access),
    db: Session = Depends(get_db)
):
    """Delete tenant"""
    await TenantService.delete_tenant(db, tenant.id)