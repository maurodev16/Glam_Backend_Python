# app/services/tenant/validations/tenant_access.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
from app.models.tenant_model import Tenant
from app.models.user_model import User
from .tenant_existence import validate_tenant

logger = logging.getLogger(__name__)

async def validate_tenant_access(db: Session, tenant_id: int, user: User) -> Tenant:
    """Validate tenant existence and user access"""
    tenant = await validate_tenant(db, tenant_id)
    
    if tenant.id != user.tenant_id:
        logger.warning(f"User {user.id} attempted to access unauthorized tenant {tenant_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this tenant"
        )
    return tenant
