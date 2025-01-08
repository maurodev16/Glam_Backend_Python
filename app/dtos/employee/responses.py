# app/dto/employee/responses.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.core.enums.enums import UserRole, StatusRole
from .requests import WorkSchedule
from uuid import UUID
class EmployeeResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    is_active: StatusRole
    specialties: Optional[List[str]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    work_schedule: Optional[List[WorkSchedule]] = None
    service_ids: List[int] = []
    created_at: datetime
    tenant_id: Optional[UUID] = None

    model_config = {
        "from_attributes": True
    }
