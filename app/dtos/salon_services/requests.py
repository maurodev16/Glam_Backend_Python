# app/dto/service/requests.py
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class CreateServiceDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    duration: Optional[Decimal] = Field(None, ge=0)
    price: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)
    estimated_duration: Optional[int] = Field(None, gt=0)
    salon_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Haircut",
                "description": "Professional haircut service",
                "duration": 30,
                "price": "50.00",
                "category": "Hair",
                "estimated_duration": 30,
                "salon_id": 1
            }
        }
    }

class UpdateServiceDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    duration: Optional[Decimal] = Field(None, ge=0)
    price: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)
    estimated_duration: Optional[int] = Field(None, gt=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Haircut",
                "price": "60.00",
                "estimated_duration": 35
            }
        }
    }
