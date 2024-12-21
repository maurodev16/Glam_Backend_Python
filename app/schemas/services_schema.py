from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration: Optional[Decimal] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    estimated_duration: Optional[int] = None
    salon_id: int

    @field_validator('price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price cannot be negative')
        return v

    @field_validator('estimated_duration')
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Duration must be positive')
        return v

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[Decimal] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    estimated_duration: Optional[int] = None

    @field_validator('price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price cannot be negative')
        return v

    @field_validator('estimated_duration')
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Duration must be positive')
        return v

class Service(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True