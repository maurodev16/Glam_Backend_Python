# app/services/tenant/validations/tenant_existence.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
import logging
from app.models.tenant_model import Tenant

logger = logging.getLogger(__name__)

async def validate_tenant(db: Session, tenant_id: int) -> Tenant:
    """Validate tenant existence and return tenant"""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        logger.error(f"Tenant not found: {tenant_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    return tenant

async def validate_tenant_id(db: Session, tenant_id: Optional[int]) -> Optional[int]:
    """Validate tenant_id in update operations"""
    if tenant_id is not None:
        if tenant_id == 0:
            return None
        
        tenant = await validate_tenant(db, tenant_id)
        return tenant.id
    return tenant_id
