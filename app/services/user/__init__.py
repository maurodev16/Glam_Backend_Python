from app.services.user.password_service import PasswordService
from app.services.user.update_service import UpdateUserService

class UserService:
    update_user = UpdateUserService.update_user
    update_password = PasswordService.update_password

__all__ = ['UserService']