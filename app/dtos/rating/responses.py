# app/dto/rating/responses.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RatingResponseDTO(BaseModel):
    id: int
    client_id: int
    salon_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "client_id": 1,
                "salon_id": 1,
                "rating": 5,
                "comment": "Excellent service!",
                "created_at": "2024-01-01T12:00:00"
            }
        }
    }
