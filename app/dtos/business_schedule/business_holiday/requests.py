from pydantic import BaseModel


class CreateHolidayRequestDTO(BaseModel):
    date: str  # Formato: YYYY-MM-DD
    description: str = None
    is_closed: bool = True
    open_time: str = None  # Formato: HH:MM:SS
    close_time: str = None  # Formato: HH:MM:SS

    class Config:
        schema_extra = {
            "example": {
                "date": "2025-01-01",
                "description": "New Year's Day",
                "is_closed": True,
                "open_time": None,
                "close_time": None
            }
        }
