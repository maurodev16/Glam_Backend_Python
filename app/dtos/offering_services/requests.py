from pydantic import BaseModel, Field, condecimal
from typing import Optional
from decimal import Decimal

# Defina os tipos personalizados
DurationType = Optional[condecimal(decimal_places=2, ge=Decimal('0'))]
PriceType = Optional[condecimal(decimal_places=2, ge=Decimal('0'))]

class CreateOfferingServiceDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    duration: DurationType
    price: PriceType
    salon_id: int
    category: Optional[str] = Field(None, max_length=100)
    estimated_duration: Optional[int] = Field(None, ge=0)

class UpdateOfferingServiceDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    duration: Optional[Decimal] = Field(None, ge=0)
    price: PriceType
    category: Optional[str] = Field(None, max_length=100)
    estimated_duration: Optional[int] = Field(None, ge=0)
