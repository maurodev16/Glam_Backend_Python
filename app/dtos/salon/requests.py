# app/dto/salon/requests.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from app.dtos.business_hours.responses import BusinessHoursResponseDTO

class CreateSalonDTO(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: EmailStr
    is_active: bool = True
    image_url: Optional[str] = None
    business_hours: Optional[List[BusinessHoursResponseDTO]] = None

class UpdateSalonDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = None
    business_hours: Optional[List[BusinessHoursResponseDTO]] = None
