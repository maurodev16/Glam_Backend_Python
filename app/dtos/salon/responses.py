from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app.dtos.business_hours.responses import BusinessHoursResponseDTO

class SalonResponseDTO(BaseModel):
    id: int
    tenant_id: int
    name: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: EmailStr
    cnpj: str
    is_public: bool
    is_active: bool
    rating: float = 0.0
    total_ratings: int = 0
    image_url: Optional[str] = None
    owner_id: int
    parent_id: Optional[int] = None
    is_headquarters: bool
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
    is_headquarters: bool
    is_active: bool

    class Config:
        from_attributes = True