# app/dto/employee/responses.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Union
from datetime import datetime
from .requests import WorkingHoursDTO

class EmployeeServiceResponseDTO(BaseModel):
    id: int
    service_id: int
    employee_id: int

    model_config = {
        "from_attributes": True
    }

class EmployeeResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    specialties: Optional[str] = None
    commission_rate: Optional[str] = None
    is_active: bool
    working_hours: Optional[Dict[str, Union[WorkingHoursDTO, None]]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    user_id: Optional[int]
    salon_id: int
    created_at: datetime
    available_services: List[EmployeeServiceResponseDTO]

    model_config = {
        "from_attributes": True
    }
