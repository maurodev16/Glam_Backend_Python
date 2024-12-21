from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
from datetime import datetime

class PortfolioItemBase(BaseModel):
    professional_id: int
    salon_id: int
    image_url: HttpUrl
    description: Optional[str] = None
    service_id: Optional[int] = None

    @field_validator('image_url')
    def validate_image_url(cls, v):
        if not str(v).lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            raise ValueError('URL must point to an image file')
        return v

class PortfolioItemCreate(PortfolioItemBase):
    pass

class PortfolioItemUpdate(BaseModel):
    image_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    service_id: Optional[int] = None

    @field_validator('image_url')
    def validate_image_url(cls, v):
        if v and not str(v).lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            raise ValueError('URL must point to an image file')
        return v

class PortfolioItem(PortfolioItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True