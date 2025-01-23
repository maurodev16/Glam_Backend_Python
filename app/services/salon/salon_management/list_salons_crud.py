# app/services/salon/service_management/list_service.py
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.dtos.offering_services.responses import ServiceOfferingResponseDTO
from app.models.salon_model import Salon

# app/services/salon/list_salons.py
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from app.models.salon_model import Salon
from app.dtos.salon.responses import SalonListResponseDTO
from app.core.enums.enums import StatusRole

class ListSalonsServiceCrud:
    @staticmethod
    async def execute(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[SalonListResponseDTO]:
        try:
            salons = db.query(Salon)\
                .options(
                    joinedload(Salon.services)  # Carrega os serviços eagerly
                )\
                .filter(Salon.is_active == StatusRole.ACTIVE)\
                .offset(skip)\
                .limit(limit)\
                .all()
            
            return [SalonListResponseDTO.model_validate(salon) for salon in salons]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
