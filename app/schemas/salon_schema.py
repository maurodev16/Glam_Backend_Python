from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.schemas.business_hours import BusinessHoursInDB

class SalonBase(BaseModel):
    name: str  = None
    description: Optional[str] = None
    address: str  = None
    city: str  = None
    state: str  = None
    zip_code: str  = None
    phone: str  = None
    email: EmailStr  = None
    is_active: bool = True
    rating: float = 0.0
    total_ratings: int = 0
    image_url: Optional[str] = None

    model_config  = {
        "from_attributes": True
    }

class SalonCreate(SalonBase):
    business_hours: Optional[List[BusinessHoursInDB]] = None

    model_config  = {
        "from_attributes": True
    }

class SalonUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    rating: Optional[float] = None
    total_ratings: Optional[int] = None
    image_url: Optional[str] = None
    business_hours: Optional[List[BusinessHoursInDB]] = None

    model_config   = {
        "from_attributes": True
    }

class SalonInDB(SalonBase):
    id: int = None
    owner_id: int = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    business_hours: Optional[List[BusinessHoursInDB] ] = None

    model_config  = {
        "from_attributes": True
    }

class SalonResponse(SalonInDB):
    model_config = {
        "from_attributes": True
    }