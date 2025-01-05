from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.models.tenant_model import Tenant

class GetTenantService:
    @staticmethod
    async def get_by_id(db: Session, tenant_id: int) -> Tenant:
        """Get tenant by ID"""
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
        return tenant

    @staticmethod
    async def list_all(db: Session) -> List[Tenant]:
        """List all tenants"""
        return db.query(Tenant).all()

    @staticmethod
    async def list_active(db: Session) -> List[Tenant]:
        """List only active tenants"""
        return db.query(Tenant).filter(Tenant.is_active == True).all()