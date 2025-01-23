from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import StringConstraints

from app.dtos.business_schedule.business_hours.requests import CreateBusinessHoursRequestDTO



DEFAULT_IMAGE_URL = "https://g5vqujw8iglfdivd.public.blob.vercel-storage.com/logo_empty-rND59FWNzO1cOzfSHOGlApp6nnllOz.png"

class CreateSalonDTO(BaseModel):
    # Salon Information
    tenant_id: Optional[UUID] = None
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    address: str = Field(..., max_length=200)
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    zip_code: str = Field(..., min_length=8)
    phone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    cnpj: Optional[Annotated[str, StringConstraints(min_length=14, max_length=14,)]] = None
    is_public: bool = True
    image_url: Optional[str] = Field(default=DEFAULT_IMAGE_URL)
    is_headquarters: bool = False
    parent_id: Optional[int] = None  # Make tenant_id optional since it will be handled automatically
    business_hours: Optional[List[CreateBusinessHoursRequestDTO]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Beauty Salon",
                "description": "A beautiful salon",
                "address": "Dr Francisco Machado de Campos",
                "number": "123",
                "city": "Limeira",
                "state": "SP",
                "zip_code": "13478998",
                "phone": "1234567890",
                "email": "salon@example.com",
                "cnpj": "12345678901234",
                "is_public": True,
                "image_url": DEFAULT_IMAGE_URL,
                "is_headquarters": False,
                "parent_id": None,
             
            }
        }

class UpdateSalonDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    address: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, min_length=2)
    state: Optional[str] = Field(None, min_length=2)
    zip_code: Optional[str] = Field(None, min_length=8)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    cnpj: Optional[Annotated[str, StringConstraints(min_length=14, max_length=14)]] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None
    is_headquarters: Optional[bool] = None
    parent_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Beauty Salon",
                "description": "An updated description",
                "address": "456 New St",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "90001",
                "phone": "9876543210",
                "email": "updated@example.com",
                "cnpj": "12345678901234",
                "is_public": True,
                "image_url": "https://example.com/image.jpg",
                "is_headquarters": False,
                "parent_id": None
            }
        }