# app/services/salon/validations/types/owner_validation_types.py
from dataclasses import dataclass
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.dtos.salon.requests import CreateSalonDTO

@dataclass
class OwnerValidationData:
    salon_data: CreateSalonDTO
    current_user: Optional[User]
    db: Session
