from pydantic import BaseModel


class DayOfWeekRequestDTO(BaseModel):
    day_name: str

    class Config:
        from_attributes = True
