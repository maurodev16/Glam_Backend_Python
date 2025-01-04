from fastapi import Depends, HTTPException, status
from app.models.user_model import User
from app.core.enums.enums import UserRole
from app.routers.auth.dependencies import get_current_user

def require_admin():
    async def admin_dependency(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user
    return admin_dependency

def require_user_access(user_id: int):
    async def user_access_dependency(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role != UserRole.ADMIN and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this user"
            )
        return current_user
    return user_access_dependency
