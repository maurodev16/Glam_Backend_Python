from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import time

class BusinessHoursBaseDTO(BaseModel):
    day_of_week_id: Optional[int] = None
    open_time: Optional[str] = None  # Alterado para string
    close_time: Optional[str] = None  # Alterado para string
    is_closed: Optional[bool] = False

    @field_validator('day_of_week_id', mode='before')
    def validate_day_of_week_id(cls, v):
        if v is not None and not 0 <= v <= 6:
            raise ValueError('day_of_week_id must be between 0 and 6')
        return v

    @model_validator(mode='after')
    def validate_times(self):
        if not self.is_closed:
            if self.open_time is None or self.close_time is None:
                raise ValueError('open_time and close_time must be provided if is_closed is False')

            # Verifica se o formato é válido
            try:
                open_time_obj = time.fromisoformat(self.open_time)
                close_time_obj = time.fromisoformat(self.close_time)
            except ValueError:
                raise ValueError('Invalid time format. Use HH:MM')

            # Verifica se os horários fazem sentido
            if close_time_obj <= open_time_obj:
                raise ValueError('close_time must be after open_time')

        return self
