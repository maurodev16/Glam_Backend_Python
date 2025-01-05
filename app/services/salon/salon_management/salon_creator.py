from sqlalchemy.orm import Session
from app.models.salon_model import Salon
from app.models.business_hours_model import BusinessHours
from app.models.user_model import User
from app.models.tenant_model import Tenant
from app.dtos.salon.requests import CreateSalonDTO
from typing import List
import logging

from app.dtos.business_hours.requests import CreateBusinessHoursDTO

logger = logging.getLogger(__name__)

class SalonCreator:
    @staticmethod
    async def create_salon(
        db: Session,
        salon_data: CreateSalonDTO,
        owner: User,
        tenant: Tenant
    ) -> Salon:
        """Create new salon with all related data"""
        salon = await SalonCreator._create_salon_record(db, salon_data, owner, tenant)
        
        if salon_data.business_hours:
            await SalonCreator._create_business_hours(db, salon.id, salon_data.business_hours)
        
        return salon

    @staticmethod
    async def _create_salon_record(
        db: Session,
        salon_data: CreateSalonDTO,
        owner: User,
        tenant: Tenant
    ) -> Salon:
        """Create the main salon record"""
        salon = Salon(
            name=salon_data.name,
            description=salon_data.description,
            address=salon_data.address,
            city=salon_data.city,
            state=salon_data.state,
            zip_code=salon_data.zip_code,
            phone=salon_data.phone,
            email=salon_data.email,
            cnpj=salon_data.cnpj,
            is_public=salon_data.is_public,
            image_url=salon_data.image_url,
            is_headquarters=salon_data.is_headquarters,
            parent_id=salon_data.parent_id,
            tenant_id=tenant.id,
            owner_id=owner.id
        )
        db.add(salon)
        db.flush()
        return salon

    @staticmethod
    async def _create_business_hours(
        db: Session,
        salon_id: int,
        business_hours_data: List[CreateBusinessHoursDTO]
    ):
        """Create business hours records"""
        for hours in business_hours_data:
            business_hours = BusinessHours(
                salon_id=salon_id,
                **hours.model_dump()
            )
            db.add(business_hours)
        db.flush()