# app/services/user/upgrade_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.models.user_model import User
from app.models.tenant_model import Tenant
from app.core.enums.enums import UserRole
from app.dtos.user.requests import UpgradeToBusinessDTO

logger = logging.getLogger(__name__)

from app.dtos.user.responses import UpgradeToBusinessResponseDTO, TenantResponseDTO

class UpgradeService:
    @staticmethod
    async def upgrade_to_business(
        db: Session,
        user_id: int,
        upgrade_data: UpgradeToBusinessDTO
    ) -> UpgradeToBusinessResponseDTO:
        try:
            # Buscar usuário
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            if user.role == UserRole.SALON_OWNER:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is already a salon owner"
                )

            # Verificar existência de Tenant
            existing_tenant = db.query(Tenant).filter(
                (Tenant.email == upgrade_data.business_email) |
                (Tenant.cnpj == upgrade_data.business_cnpj)
            ).first()
            if existing_tenant:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A tenant with this email or CNPJ already exists"
                )

            # Criar novo Tenant
            tenant = Tenant(
                business_name=upgrade_data.business_name,
                email=upgrade_data.business_email or user.email,
                phone=upgrade_data.business_phone or user.phone,
                cnpj=upgrade_data.business_cnpj,
                cpf=upgrade_data.business_cpf,
                address=upgrade_data.business_address
            )
            db.add(tenant)
            db.flush()

            # Atualizar papel do usuário e associar Tenant
            user.role = UserRole.SALON_OWNER
            user.tenant_id = tenant.id

            db.commit()
            db.refresh(user)

            # Construir o TenantResponseDTO
            tenant_dto = TenantResponseDTO(
                id=tenant.id,
                business_name=tenant.business_name,
                email=tenant.email,
                phone=tenant.phone,
                cnpj=tenant.cnpj,
                cpf=tenant.cpf,
                address=tenant.address,
                is_active=tenant.is_active.value,
                is_verified=tenant.is_verified,
                created_at=tenant.created_at,
                updated_at=tenant.updated_at
            )

            # Construir o UpgradeToBusinessResponseDTO
            response_dto = UpgradeToBusinessResponseDTO(
                user_id=user.id,
                name=user.name,
                email=user.email,
                phone=user.phone,
                role=user.role.value,
                tenant=tenant_dto,
                updated_at=user.updated_at
            )

            return response_dto

        except Exception as e:
            db.rollback()
            logger.error(f"Error upgrading user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while upgrading the user"
            )
