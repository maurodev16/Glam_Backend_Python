# app/dto/commission/requests.py
from pydantic import BaseModel, Field, confloat, field_validator
from app.models.commission_model import CommissionType
from typing import Union

class CreateCommissionDTO(BaseModel):
    employee_id: int
    commission_type: CommissionType
    value: float = Field(gt=0)

    @field_validator('value')
    def validate_value(cls, v, values):
        if 'commission_type' in values:
            if values['commission_type'] == CommissionType.PERCENTAGE:
                if v > 100:
                    raise ValueError('Percentage value must be between 0 and 100')
            elif values['commission_type'] == CommissionType.FIXED:
                if v <= 0:
                    raise ValueError('Fixed value must be greater than 0')
        return v

class UpdateCommissionDTO(BaseModel):
    commission_type: CommissionType | None = None
    value: float | None = Field(None, gt=0)

    @field_validator('value')
    def validate_value(cls, v, values):
        if v is not None and 'commission_type' in values:
            if values['commission_type'] == CommissionType.PERCENTAGE:
                if v > 100:
                    raise ValueError('Percentage value must be between 0 and 100')
            elif values['commission_type'] == CommissionType.FIXED:
                if v <= 0:
                    raise ValueError('Fixed value must be greater than 0')
        return v
