# app/dto/business_hours/responses.py
from pydantic import BaseModel
from datetime import time

class BusinessHoursResponseDTO(BaseModel):
    id: int
    salon_id: int
    day_of_week: int
    open_time: time
    close_time: time
    is_closed: bool

    class Config:
        from_attributes = True
