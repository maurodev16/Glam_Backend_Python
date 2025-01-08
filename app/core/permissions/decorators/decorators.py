# app/core/permissions/decorators.py
from functools import wraps
from fastapi import Depends, HTTPException
from app.models.user_model import User
from app.models.salon_model import Salon
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.core.permissions.salon_permissions import SalonPermissions
from app.routers.auth.dependencies.dependecies import get_current_user
from app.core.exceptions.permission import PermissionDenied

async def require_salon_owner(
    salon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to require salon owner permission"""
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if not salon:
        raise HTTPException(status_code=404, detail="Salon not found")
        
    if not SalonPermissions.verify_salon_owner(current_user, salon):
        raise HTTPException(status_code=403, detail="Must be salon owner")
        
    return current_user

def require_can_rate():
    """Decorator to require rating permission"""
    async def dependency(
        salon_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> User:
        salon = db.query(Salon).filter(Salon.id == salon_id).first()
        if not salon:
            raise HTTPException(status_code=404, detail="Salon not found")
            
        if not SalonPermissions.verify_can_rate_salon(current_user, salon):
            raise PermissionDenied("Must complete appointment before rating")
            
        return current_user
    return Depends(dependency)