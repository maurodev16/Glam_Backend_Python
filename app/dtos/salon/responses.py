# app/dto/salon/responses.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app.dtos.business_hours.responses import BusinessHoursResponseDTO


class SalonResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: EmailStr
    is_active: bool
    rating: float = 0.0
    total_ratings: int = 0
    image_url: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    business_hours: Optional[List[BusinessHoursResponseDTO]] = None

    class Config:
        from_attributes = True

class SalonListResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    city: str
    state: str
    rating: float = 0.0
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
