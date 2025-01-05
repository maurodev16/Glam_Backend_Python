# app/services/tenant/validation_service.py

from app.dtos.salon.requests import CreateSalonDTO
from app.dtos.tenant.requests import CreateTenantDTO
from app.services.tenant import TenantService
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.tenant_model import Tenant

class TenantValidationService:
    @staticmethod
    async def get_or_create_tenant(
        db: Session, 
        salon_data: CreateSalonDTO,
        owner: User
    ) -> Tenant:
        """Get existing tenant or create new one"""
        # If tenant_id provided, validate and return
        if salon_data.tenant_id:
            return await TenantValidationService.validate_tenant(db, salon_data.tenant_id)
            
        # Check if owner already has a tenant
        if owner.tenant_id:
            return await TenantValidationService.validate_tenant(db, owner.tenant_id)
            
        # Create new tenant
        tenant_data = CreateTenantDTO(
            business_name=salon_data.name,
            email=salon_data.email,
            phone=salon_data.phone,
            document_type="cnpj",
            document=salon_data.cnpj,
        )
        
        return await TenantService.create_tenant(db, tenant_data)
