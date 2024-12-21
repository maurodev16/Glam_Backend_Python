from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime, time
from enum import Enum
from .professional_schema import Professional
from .client_schema import Client
from .services_schema import Service

class AppointmentStatus(str, Enum):
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class AppointmentBase(BaseModel):
    professional_id: int
    client_id: int
    service_id: int
    salon_id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus

    @field_validator('appointment_date')
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError('Appointment date cannot be in the past')
        return v

    @field_validator('appointment_time')
    def validate_time(cls, v):
        # Basic time validation - can be enhanced based on business hours
        business_start = time(hour=9, minute=0)
        business_end = time(hour=17, minute=0)
        
        if v < business_start or v > business_end:
            raise ValueError('Appointment time must be between 9:00 and 17:00')
        return v

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[AppointmentStatus] = None

    @field_validator('appointment_date')
    def validate_update_date(cls, v):
        if v and v < date.today():
            raise ValueError('Appointment date cannot be in the past')
        return v

    @field_validator('appointment_time')
    def validate_update_time(cls, v):
        if v:
            business_start = time(hour=9, minute=0)
            business_end = time(hour=17, minute=0)
            
            if v < business_start or v > business_end:
                raise ValueError('Appointment time must be between 9:00 and 17:00')
        return v

class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentDetail(AppointmentResponse):
    professional: Optional[Professional] = None
    client: Optional[Client] = None
    service: Optional[Service] = None

    class Config:
        from_attributes = True
