from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.core.enums.enums import UserRole, StatusRole
from app.dtos.tenant import requests
from app.dtos.tenant.responses import TenantResponseDTO

class UserResponseDTO(BaseModel):
    id: int
    name: str
    phone: str
    role: UserRole
    is_active: StatusRole
    created_at: datetime
    tenant: Optional[TenantResponseDTO] = None

class UpgradeToBusinessResponseDTO(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    phone: str
    role: str  # CLIENT, SALON_OWNER, etc.
    tenant: TenantResponseDTO
    updated_at: datetime
    
class Config:
    from_attributes = True