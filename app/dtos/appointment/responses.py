from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional
from app.dtos.user.responses import UserResponseDTO

from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class AppointmentResponseDTO(BaseModel):
    id: int
    employee_id: int
    user_id: int
    service_id: int
    salon_id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentDetailDTO(AppointmentResponseDTO):
    employee: Optional[employeeResponseDTO] = None
    user: Optional[UserResponseDTO] = None
    service: Optional[ServiceResponseDTO] = None

    class Config:
        from_attributes = True
