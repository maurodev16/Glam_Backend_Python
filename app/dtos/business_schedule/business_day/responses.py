from pydantic import BaseModel

class DayOfWeekResponseDTO(BaseModel):
    id: int
    day_name: str

    class Config:
        from_attributes = True