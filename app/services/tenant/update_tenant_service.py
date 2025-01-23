from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.tenant_model import Tenant
from app.dtos.tenant.requests import UpdateTenantDTO

class UpdateTenantService:
    @staticmethod
    async def update(db: Session, tenant_id: int, tenant_data: UpdateTenantDTO) -> Tenant:
        """Update tenant information"""
        tenant = await UpdateTenantService._get_tenant(db, tenant_id)
        return await UpdateTenantService._update_tenant(db, tenant, tenant_data)
    
    @staticmethod
    async def _get_tenant(db: Session, tenant_id: str) -> Tenant:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
        return tenant
    
    @staticmethod
    async def _update_tenant(db: Session, tenant: Tenant, tenant_data: UpdateTenantDTO) -> Tenant:
        for field, value in tenant_data.model_dump(exclude_unset=True).items():
            setattr(tenant, field, value)
        db.commit()
        db.refresh(tenant)
        return tenant