# app/dto/rating/requests.py
from pydantic import BaseModel, Field
from typing import Optional

class CreateRatingDTO(BaseModel):
    user_id: int
    salon_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating value between 1 and 5")
    comment: Optional[str] = Field(None, max_length=500)

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "salon_id": 1,
                "rating": 5,
                "comment": "Excellent service!"
            }
        }
    }

class UpdateRatingDTO(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating value between 1 and 5")
    comment: Optional[str] = Field(None, max_length=500)

    model_config = {
        "json_schema_extra": {
            "example": {
                "rating": 4,
                "comment": "Updated review - Very good service"
            }
        }
    }
