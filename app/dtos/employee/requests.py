# app/dto/employee/requests.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Union
from datetime import time

class WorkingHoursDTO(BaseModel):
    start: time
    end: time

class WorkingScheduleDTO(BaseModel):
    monday: Optional[WorkingHoursDTO]
    tuesday: Optional[WorkingHoursDTO]
    wednesday: Optional[WorkingHoursDTO]
    thursday: Optional[WorkingHoursDTO]
    friday: Optional[WorkingHoursDTO]
    saturday: Optional[WorkingHoursDTO]
    sunday: Optional[WorkingHoursDTO]

class CreateEmployeeDTO(BaseModel):
    name: str
    email: EmailStr
    phone: str
    specialties: Optional[str] = None
    commission_rate: Optional[str] = None
    working_hours: Optional[Dict[str, Union[WorkingHoursDTO, None]]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    salon_id: int
    user_id: Optional[int] = None
    service_ids: List[int] = []

class UpdateEmployeeDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    specialties: Optional[str] = None
    commission_rate: Optional[str] = None
    working_hours: Optional[Dict[str, Union[WorkingHoursDTO, None]]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    service_ids: Optional[List[int]] = None
