# backend/app/routers/users/routes/status.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import user_permissions
from ....core.database import get_db
from ....models import user_model as models
from app.dtos.user import responses

from ...auth.dependencies import get_current_user
from ....core.enums.enums import StatusRole, UserRole

router = APIRouter()

@router.patch("/{user_id}/status", response_model=responses.UserResponseDTO)
async def update_user_status(
    user_id: int,
    status: StatusRole,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user status (admin only)"""
    if not user_permissions(current_user, [UserRole.ADMIN]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = status
    db.commit()
    db.refresh(user)
    return user
