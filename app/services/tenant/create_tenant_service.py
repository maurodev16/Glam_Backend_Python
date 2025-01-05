from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.tenant_model import Tenant
from app.dtos.tenant.requests import CreateTenantDTO

class CreateTenantService:
    @staticmethod
    async def create(db: Session, tenant_data: CreateTenantDTO) -> Tenant:
        """Create a new tenant"""
        await CreateTenantService._validate_unique_document(db, tenant_data.document)
        return await CreateTenantService._save_tenant(db, tenant_data)
    
    @staticmethod
    async def _validate_unique_document(db: Session, document: str):
        if db.query(Tenant).filter(Tenant.document == document).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document already registered"
            )
    
    @staticmethod
    async def _save_tenant(db: Session, tenant_data: CreateTenantDTO) -> Tenant:
        tenant = Tenant(**tenant_data.model_dump())
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        return tenant