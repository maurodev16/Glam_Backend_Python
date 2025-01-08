from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import Optional
import logging

from app.models.user_model import User
from app.models.salon_model import Salon
from app.dtos.salon.requests import CreateSalonDTO
from app.services.salon.salon_management.tenant_handler import TenantHandler
from .tenant_validator import TenantValidationService
from .owner_handler import OwnerHandler
from .salon_creator import SalonCreator

logger = logging.getLogger(__name__)

class CreateSalonServiceCrud:
    @staticmethod
    async def execute(
        db: Session,
        salon_data: CreateSalonDTO,
        current_user: Optional[User] = None
    ) -> Salon:
        """Orchestrate salon creation process"""
        try:
            # Validar ou criar o proprietário
            owner = await OwnerHandler.handle_owner(
                db=db,
                salon_data=salon_data,
                current_user=current_user
            )
            
            # Validar ou criar o tenant associado
            tenant = await TenantHandler.handle_tenant(
                db=db,
                salon_data=salon_data,
                owner=owner
            )
            
            # Criar o salão
            salon = await SalonCreator.create_salon(
                db=db,
                salon_data=salon_data,
                owner=owner,
                tenant=tenant
            )
            
            # Persistir alterações no banco de dados
            db.commit()
            db.refresh(salon)  # Atualizar o objeto após commit
            
            return salon
            
        except SQLAlchemyError as e:
            logger.error(f"Erro no banco de dados ao criar o salão: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar o salão. Tente novamente mais tarde."
            )
