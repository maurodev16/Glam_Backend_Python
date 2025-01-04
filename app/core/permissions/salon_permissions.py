# app/core/permissions/salon_permissions.py
from typing import Optional
from fastapi import HTTPException, status
from app.models.user_model import User
from app.models.salon_model import Salon
from app.core.enums.enums import UserRole

class SalonPermissions:
    @staticmethod
    def verify_salon_owner(user: User, salon: Salon) -> bool:
        """Verify if user owns the salon"""
        if user.role != UserRole.SALON_OWNER:
            return False
        return user.tenant_id == salon.tenant_id

    @staticmethod
    def verify_can_rate_salon(user: User, salon: Salon) -> bool:
        """Verify if user can rate the salon"""
        # Add logic to check if user has completed appointments
        return True  # Implement your logic here

    @staticmethod
    def verify_can_manage_employees(user: User, salon: Salon) -> bool:
        """Verify if user can manage salon employees"""
        return SalonPermissions.verify_salon_owner(user, salon)

    @staticmethod
    def verify_can_manage_services(user: User, salon: Salon) -> bool:
        """Verify if user can manage salon services"""
        return SalonPermissions.verify_salon_owner(user, salon)
