# app/core/validators/base_validator.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

class BaseValidator:
    @staticmethod
    async def validate_unique_field(
        db: Session,
        model: any,
        field: str,
        value: str,
        exclude_id: Optional[int] = None
    ) -> bool:
        """Generic unique field validator"""
        query = db.query(model).filter(getattr(model, field) == value)
        if exclude_id:
            query = query.filter(model.id != exclude_id)
        return query.first() is None
