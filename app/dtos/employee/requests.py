# app/dto/employee/requests.py
from pydantic import BaseModel, EmailStr, Field, confloat
from typing import Optional, List
from datetime import time
from app.core.enums.enums import CommissionType

class WorkSchedule(BaseModel):
    day: str
    start_time: time
    end_time: time

class CommissionData(BaseModel):
    commission_type: CommissionType
    value: float = Field(..., gt=0, le=100)  # Percentage (0-100) or fixed amount

class CreateEmployeeDTO(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    specialties: Optional[List[str]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    work_schedule: Optional[List[WorkSchedule]] = None
    service_ids: List[int] = []
    commission: CommissionData

class UpdateEmployeeDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    specialties: Optional[List[str]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    work_schedule: Optional[List[WorkSchedule]] = None
    service_ids: Optional[List[int]] = None
    commission: Optional[CommissionData] = None
