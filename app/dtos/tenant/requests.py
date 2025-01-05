from pydantic import BaseModel, EmailStr, Field
from app.core.enums.enums import DocumentType

class CreateTenantDTO(BaseModel):
    business_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)
    document_type: DocumentType
    document: str = Field(min_length=11, max_length=14)  # 11 para CPF, 14 para CNPJ

class UpdateTenantDTO(BaseModel):
    business_name: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, min_length=10, max_length=15)
    is_active: bool | None = None