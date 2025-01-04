# app/core/permissions/user_permissions.py
from typing import List
from app.models.user_model import User
from app.core.enums.enums import UserRole

class UserPermissions:
    @staticmethod
    def can_list_users(user: User) -> bool:
        return user.role == UserRole.ADMIN
        
    @staticmethod
    def can_view_user(user: User, target_user_id: int) -> bool:
        return user.role == UserRole.ADMIN or user.id == target_user_id
        
    @staticmethod
    def can_delete_user(user: User) -> bool:
        return user.role == UserRole.ADMIN
        
    @staticmethod
    def can_update_user(user: User, target_user_id: int) -> bool:
        return user.role == UserRole.ADMIN or user.id == target_user_id
