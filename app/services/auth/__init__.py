from .register_service import RegisterService
from .login_service import LoginService

class AuthService:
    register = RegisterService.register_user
    login = LoginService.login_user

__all__ = ['AuthService']