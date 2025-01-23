from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.core.enums.enums import StatusRole
from app.dtos.offering_services.responses import ServiceOfferingResponseDTO
from app.dtos.business_schedule.business_day.responses import DayOfWeekResponseDTO
from app.dtos.business_schedule.business_holiday.responses import CreatedHolidayResponseDTO
from app.dtos.business_schedule.business_hours.responses import CreatedBusinessHoursResponseDTO

class SalonResponseDTO(BaseModel):
    id: int
    tenant_id: UUID
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
    is_active: StatusRole
    rating: float = 0.0
    total_ratings: int = 0
    image_url: Optional[str] = None
    owner_id: int
    parent_id: Optional[int] = None
    is_headquarters: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    business_hours: Optional[List[CreatedBusinessHoursResponseDTO]] = []
    services: Optional[List[ServiceOfferingResponseDTO]] = []
    business_days: Optional[List[DayOfWeekResponseDTO]] = []
    holidays: Optional[List[CreatedHolidayResponseDTO]] = []

    class Config:
        from_attributes = True

class SalonListResponseDTO(BaseModel):
    id: int
    #tenant_id: UUID
    name: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: EmailStr
    #cnpj: str
    #is_public: bool
    #is_active: StatusRole
    rating: float = 0.0
    total_ratings: int = 0
    image_url: Optional[str] = None
    #owner_id: int
    #parent_id: Optional[int] = None
    #is_headquarters: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    business_hours: Optional[List[CreatedBusinessHoursResponseDTO]] = []
    services: Optional[List[ServiceOfferingResponseDTO]] = []
    business_days: Optional[List[DayOfWeekResponseDTO]] = []
    holidays: Optional[List[CreatedHolidayResponseDTO]] = []

    class Config:
        from_attributes = True