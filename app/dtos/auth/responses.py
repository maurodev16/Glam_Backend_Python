from pydantic import BaseModel
from datetime import datetime

from app.core.enums.enums import StatusRole

class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class AuthUserResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str
    is_active: StatusRole
    created_at: datetime    
    
        
class Config:
    from_attributes = True