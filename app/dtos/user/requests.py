from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from app.core.enums.enums import UserRole, StatusRole

class UpdateUserDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[StatusRole] = None
    tenant_id: Optional[int] = None


class UpgradeToBusinessDTO(BaseModel):
    business_name: str = Field(..., min_length=3)
    business_email: EmailStr
    business_phone: str
    business_cnpj: str = Field(None, pattern=r"^\d{14}$")  # Opcional
    business_cpf: str = Field(None, pattern=r"^\d{11}$")  # Opcional
    business_address: str


class UpdatePasswordDTO(BaseModel):
    current_password: str
    new_password: str