from pydantic import BaseModel
from datetime import datetime
from app.models.commission_model import CommissionType
from app.dtos.user.responses import UserResponseDTO

class CommissionResponseDTO(BaseModel):
    id: int
    employee_id: int
    salon_id: int
    commission_type: CommissionType
    value: float
    created_at: datetime
    updated_at: datetime
    employee: UserResponseDTO

    class Config:
        from_attributes = True
    