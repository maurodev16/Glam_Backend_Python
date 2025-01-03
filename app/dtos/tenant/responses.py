from pydantic import BaseModel
from datetime import datetime
from app.core.enums.enums import StatusRole

class TenantResponseDTO(BaseModel):
    id: int
    business_name: str
    email: str
    phone: str
    is_active: StatusRole
    created_at: datetime
    
    class Config:
        from_attributes = True