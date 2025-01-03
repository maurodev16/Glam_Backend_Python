# app/dto/service/responses.py
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ServiceResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    duration: Optional[Decimal] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    estimated_duration: Optional[int] = None
    salon_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Haircut",
                "description": "Professional haircut service",
                "duration": 30,
                "price": "50.00",
                "category": "Hair",
                "estimated_duration": 30,
                "salon_id": 1,
                "created_at": "2024-01-01T12:00:00"
            }
        }
    }
