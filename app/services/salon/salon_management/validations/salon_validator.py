# app/services/salon/validations/salon_validator.py
from app.core.validators.base_validator import BaseValidator
from app.models.salon_model import Salon
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.dtos.salon.requests import CreateSalonDTO

class SalonValidator(BaseValidator):
    @staticmethod
    async def validate_unique_fields(db: Session, salon_data: CreateSalonDTO):
        """Validate salon unique fields"""
        validations = [
            ('email', salon_data.email, "Email already registered"),
            ('phone', salon_data.phone, "Phone already registered"),
            ('cnpj', salon_data.cnpj, "CNPJ already registered")
        ]

        for field, value, message in validations:
            if value and not await BaseValidator.validate_unique_field(db, Salon, field, value):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )
