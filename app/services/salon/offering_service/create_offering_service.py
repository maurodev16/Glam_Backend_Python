from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.dtos.offering_services.requests import CreateOfferingServiceDTO
from app.models.offering_services_model import OfferingService
from app.models.user_model import User
from app.models.salon_model import Salon

class CreateOfferingService:
    @staticmethod
    async def execute(
        db: Session, 
        salon_id: int,
        service_data: CreateOfferingServiceDTO,
        current_user: User
    ) -> OfferingService:
        """Create a new service"""
        # Verificar se o salão existe
        salon = db.query(Salon).filter(Salon.id == salon_id).first()
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Salon not found"
            )
        
        # Verificar se o usuário atual é o dono do salão
        if salon.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only salon owner can create services"
            )

        # Criar o serviço
        try:
            service = OfferingService(
                salon_id=salon_id,  # Associar ao salão correto
                **service_data.model_dump()  # Desempacotar os dados do DTO
            )
            db.add(service)
            db.commit()
            db.refresh(service)
            return service
        
        except Exception as e:
            db.rollback()  # Reverter a transação em caso de erro
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating service: {str(e)}"
            )
