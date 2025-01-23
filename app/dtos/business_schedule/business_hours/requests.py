# app/dto/business_hours/requests.py
from app.dtos.business_schedule.business_hours_base_DTO import BusinessHoursBaseDTO

class CreateBusinessHoursRequestDTO(BusinessHoursBaseDTO):
    day_of_week_id: int
    open_time: str  # formato "HH:MM"
    close_time: str  # formato "HH:MM"

    class Config:
        schema_extra = {
            "example": {
                "day_of_week_id": 0,
                "open_time": "09:00:00",
                "close_time": "18:00:00",
            }
        }


class UpdateBusinessHoursRequetsDTO(BusinessHoursBaseDTO):
    class Config:
        schema_extra = {
            "example": {
                "day_of_week_id": 1,
                "open_time": "10:00:00",
                "close_time": "17:00:00",
                "is_closed": True
            }
        }
