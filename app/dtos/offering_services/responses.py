from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

class ServiceOfferingResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str]
    duration: Optional[Decimal]
    price: Optional[Decimal]
    salon_id: int
    category: Optional[str]
    estimated_duration: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True