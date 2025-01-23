from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreatedHolidayResponseDTO(BaseModel):
    id: int
    date: str
    is_closed: bool
    open_time: Optional[str] = None  # formato "HH:MM"
    close_time: Optional[str] = None  # formato "HH:MM"

    class Config:
        from_attributes = True
