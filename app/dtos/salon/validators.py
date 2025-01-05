from pydantic import field_validator
from typing import Dict, Any, Optional

from app.core.validations.document_validator import validate_document

class SalonValidators:
    @field_validator('parent_id')
    def validate_parent_id(cls, v: Optional[int], values: Dict[str, Any]) -> Optional[int]:
        if v is not None and values.get('is_headquarters'):
            raise ValueError("Headquarters cannot have a parent salon")
        return v
    
    @field_validator('owner_name', 'owner_email', 'owner_phone', 'owner_password')
    def validate_owner_fields(cls, v: Optional[str], values: Dict[str, Any], field: Dict[str, Any]) -> Optional[str]:
        if not values.get('use_existing_user') and not values.get('use_same_contact_info') and v is None:
            raise ValueError(f"{field.name} is required when creating a new user")
        return v
    
    @field_validator('cnpj')
    def validate_cnpj(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not validate_document('cnpj', v):
            raise ValueError("Invalid CNPJ number")
        return v