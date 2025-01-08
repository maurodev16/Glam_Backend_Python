from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

from app.dtos.categories.responses import CategoryResponseDTO

class ServiceOfferingResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str]
    duration: Optional[Decimal]
    price: Optional[Decimal]
    salon_id: int
    category: Optional[CategoryResponseDTO]
    estimated_duration: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True