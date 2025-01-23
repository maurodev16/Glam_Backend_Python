from pydantic import BaseModel

class CreatedBusinessHoursResponseDTO(BaseModel):
    id: int
    salon_id: int
    day_of_week_id: int
    open_time: str
    close_time: str

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 0,
                "business_day_id": 0,
                "open_time": "09:00:00",
                "close_time": "17:00:00",
            }
        }
