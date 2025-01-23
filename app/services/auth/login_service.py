from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
import logging
from typing import Optional
from app.dtos.auth.requests import LoginDTO
from app.dtos.auth.responses import TokenResponseDTO
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.user_model import User
from app.core.config import get_settings
from app.core.enums.enums import StatusRole
settings = get_settings()
logger = logging.getLogger(__name__)
class AuthenticationError(HTTPException):
    """Base class for authentication errors"""
    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=detail)
        logger.error(f"Authentication error: {detail}")
class InvalidEmailError(AuthenticationError):
    """Raised when email is not found"""
    def __init__(self):
        super().__init__(detail="Email não encontrado")
class InvalidPasswordError(AuthenticationError):
    """Raised when password is incorrect"""
    def __init__(self):
        super().__init__(detail="Senha incorreta")
class InactiveUserError(AuthenticationError):
    """Raised when user account is inactive"""
    def __init__(self):
        super().__init__(detail="Conta de usuário inativa")
class LoginService:
    @staticmethod
    async def login_user(db: Session, login_data: LoginDTO, response: Response) -> TokenResponseDTO:
        """Authenticate user and generate tokens"""
        try:
            user = await LoginService._validate_email(db, login_data.email)
            await LoginService._validate_password(login_data.password, user.password)
            await LoginService._validate_user_status(user)
            
            return await LoginService._handle_successful_login(user, response)
            
        except AuthenticationError as e:
            # Já registrado no log pela classe AuthenticationError
            raise e
        except Exception as e:
            logger.error(f"Unexpected login error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor durante o login"
            )
    @staticmethod
    async def _validate_email(db: Session, email: str) -> User:
        """Validate email and return user if found"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise InvalidEmailError()
        return user
    @staticmethod
    async def _validate_password(provided_password: str, stored_password: str) -> None:
        """Validate if provided password matches stored password"""
        if not verify_password(provided_password, stored_password):
            raise InvalidPasswordError()
    @staticmethod
    async def _validate_user_status(user: User) -> None:
        """Validate if user account is active"""
        if user.is_active == StatusRole.INACTIVE:
            raise InactiveUserError()
    @staticmethod
    async def _handle_successful_login(user: User, response: Response) -> TokenResponseDTO:
        """Handle successful login by setting tokens"""
        try:
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "tenant_id": str(user.tenant_id),
                "role": user.role.value
            }
            
            access_token = create_access_token(data=token_data)
            refresh_token = create_refresh_token(data=token_data)
            
            # Configurar cookies com tokens
            LoginService._set_auth_cookies(
                response=response,
                access_token=access_token,
                refresh_token=refresh_token
            )
            
            return TokenResponseDTO(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer"
            )
            
        except Exception as e:
            logger.error(f"Error generating tokens: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar tokens de autenticação"
            )
    @staticmethod
    def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
        """Set authentication cookies in response"""
        cookie_settings = {
            "httponly": True,
            "secure": settings.ENVIRONMENT == "production",
            "samesite": "lax"
        }
        
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            **cookie_settings
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            **cookie_settings
        )