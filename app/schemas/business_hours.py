from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional
from datetime import time

class BusinessHoursBase(BaseModel):
    day_of_week: int
    open_time: time
    close_time: time
    is_closed: bool = False

    @field_validator('day_of_week')
    def validate_day_of_week(cls, v):
        if not 0 <= v <= 6:
            raise ValueError('day_of_week must be between 0 and 6')
        return v

    model_validator(mode='after')
    def validate_times(self):
        if not self.is_closed and self.close_time <= self.open_time:
            raise ValueError('close_time must be after open_time')
        return self

class BusinessHoursCreate(BusinessHoursBase):
    pass

class BusinessHoursUpdate(BaseModel):
    day_of_week: Optional[int] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    is_closed: Optional[bool] = None

    @field_validator('day_of_week')
    def validate_day_of_week(cls, v):
        if v is not None and not 0 <= v <= 6:
            raise ValueError('day_of_week must be between 0 and 6')
        return v

    @model_validator(mode='after')
    def validate_times(self):
        if (self.open_time is not None and 
            self.close_time is not None and 
            not self.is_closed and 
            self.close_time <= self.open_time):
            raise ValueError('close_time must be after open_time')
        return self

class BusinessHoursInDB(BusinessHoursBase):
    id: int
    salon_id: int

    class Config:
        from_attributes = True