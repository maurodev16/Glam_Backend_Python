from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.tenant_model import Tenant
from app.models.user_model import User
from app.routers.auth.dependencies.dependecies import get_current_user

async def get_tenant_by_id(
    tenant_id: int,
    db: Session = Depends(get_db)
) -> Tenant:
    """Get tenant by ID"""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    return tenant

async def verify_tenant_access(
    tenant: Tenant = Depends(get_tenant_by_id),
    current_user: User = Depends(get_current_user)
) -> Tenant:
    """Verify if user has access to tenant"""
    if tenant.id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this tenant"
        )
    return tenant