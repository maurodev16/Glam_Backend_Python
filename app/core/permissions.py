# app/core/permissions.py
from typing import List, Union
from fastapi import HTTPException, status
from functools import wraps

from ..core.enums.enums import UserRole
from ..models.user_model import User

class PermissionDenied(HTTPException):
    def __init__(self, detail: str = "Você não tem permissão para realizar esta ação"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

def check_permissions(user: User, allowed_roles: List[UserRole]) -> bool:
    """Check if user has permission based on their role."""
    try:
        user_role = UserRole(user.role)
        return user_role in allowed_roles
    except ValueError:
        return False

def require_roles(*roles: UserRole):
    """Decorator to check if user has required roles."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User, **kwargs):
            if not check_permissions(current_user, list(roles)):
                raise PermissionDenied()
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Specific permission checks
def is_salon_owner(user: User) -> bool:
    """Check if user is a salon owner."""
    return check_permissions(user, [UserRole.SALON_OWNER])

def is_admin(user: User) -> bool:
    """Check if user is an admin."""
    return check_permissions(user, [UserRole.ADMIN])

def can_manage_salon(user: User, salon_tenant_id: int) -> bool:
    """Check if user can manage a specific salon."""
    if is_admin(user):
        return True
    return is_salon_owner(user) and user.tenant_id == salon_tenant_id

def verify_salon_access(user: User, salon_tenant_id: int):
    """Verify if user can access salon, raise exception if not."""
    if not can_manage_salon(user, salon_tenant_id):
        raise PermissionDenied("Você não tem permissão para acessar este salão")
