# app/services/salon/create/tenant_handler.py
from sqlalchemy.orm import Session
from typing import Optional
from app.models.tenant_model import Tenant
from app.models.user_model import User
from app.dtos.salon.requests import CreateSalonDTO
from app.dtos.tenant.requests import CreateTenantDTO
from app.services.tenant import TenantService
import logging

from app.services.salon.salon_management.tenant_validator import TenantValidationService

logger = logging.getLogger(__name__)

class TenantHandler:
    @staticmethod
    async def handle_tenant(
        db: Session,
        salon_data: CreateSalonDTO,
        owner: User
    ) -> Tenant:
        """Handle tenant creation or validation"""
        # If owner already has a tenant, use it
        if owner.tenant_id:
            logger.info(f"Using existing tenant {owner.tenant_id} for user {owner.id}")
            return await TenantValidationService.validate_tenant(db, owner.tenant_id)
        
        # If tenant_id is provided, validate it
        if salon_data.tenant_id:
            logger.info(f"Validating provided tenant {salon_data.tenant_id}")
            return await TenantValidationService.validate_tenant(db, salon_data.tenant_id)
            
        # Create new tenant for first salon
        logger.info(f"Creating new tenant for user {owner.id}")
        if not salon_data.cnpj:
            raise ValueError("CNPJ is required for creating a new tenant")
            
        tenant_data = CreateTenantDTO(
            business_name=salon_data.name,
            email=salon_data.email,
            phone=salon_data.phone,
            document_type="cnpj",
            document=salon_data.cnpj,
        )
        
        tenant = await TenantService.create_tenant(db, tenant_data)
        
        # Associate owner with new tenant
        owner.tenant_id = tenant.id
        db.flush()
        
        return tenant
