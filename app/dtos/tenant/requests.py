from typing import Optional
from pydantic import BaseModel, EmailStr, StringConstraints

class CreateTenantDTO(BaseModel):
    business_name: str
    email: EmailStr
    phone: str

class UpdateTenantDTO(BaseModel):
    business_name: Optional[str] | None = None
    email: EmailStr | None = None
    phone: Optional[str] | None = None