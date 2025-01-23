from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
import logging
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.tenant_model import Tenant
from app.models.user_model import User

logger = logging.getLogger(__name__)

class TenantValidationService:
    @staticmethod
    async def validate_tenant(db: Session, tenant_id: str) -> Tenant:
        """Validate tenant existence and return tenant"""
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            logger.error(f"Tenant not found: {tenant_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
        return tenant

    @staticmethod
    async def validate_tenant_access(db: Session, tenant_id: str, user: User) -> Tenant:
        """Validate tenant existence and user access"""
        tenant = await TenantValidationService.validate_tenant(db, tenant_id)
        
        if tenant.id != user.tenant_id:
            logger.warning(f"User {user.id} attempted to access unauthorized tenant {tenant_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this tenant"
            )
        return tenant

    @staticmethod
    async def validate_tenant_id(db: Session, tenant_id: Optional[str]) -> Optional[str]:
        """Validate tenant_id in update operations"""
        if tenant_id is not None:
            if tenant_id == "":
                return None
            
            tenant = await TenantValidationService.validate_tenant(db, tenant_id)
            return tenant.id
        return tenant_id