from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from datetime import datetime

class WorkingHours(BaseModel):
    start: str
    end: str

class WorkingSchedule(BaseModel):
    monday: Optional[WorkingHours]
    tuesday: Optional[WorkingHours]
    wednesday: Optional[WorkingHours]
    thursday: Optional[WorkingHours]
    friday: Optional[WorkingHours]
    saturday: Optional[WorkingHours]
    sunday: Optional[WorkingHours]

class ProfessionalServiceBase(BaseModel):
    service_id: int

class ProfessionalServiceCreate(ProfessionalServiceBase):
    pass

class ProfessionalService(ProfessionalServiceBase):
    id: int
    professional_id: int

    class Config:
        orm_mode = True

class ProfessionalBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialties: Optional[str] = None
    commission_rate: Optional[str] = None
    is_active: bool = True
    working_hours: Optional[Dict[str, Union[WorkingHours, None]]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

class ProfessionalCreate(ProfessionalBase):
    salon_id: int
    user_id: Optional[int] = None
    service_ids: List[int] = []

class ProfessionalUpdate(ProfessionalBase):
    service_ids: Optional[List[int]] = None

class Professional(ProfessionalBase):
    id: int
    user_id: Optional[int]
    salon_id: int
    created_at: datetime
    available_services: List[ProfessionalService]

    class Config:
        orm_mode = True