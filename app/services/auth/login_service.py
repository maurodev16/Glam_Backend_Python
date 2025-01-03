from multiprocessing import AuthenticationError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response
import logging

from app.dtos.auth.requests import LoginDTO
from app.dtos.auth.responses import TokenResponseDTO
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.user_model import User
from app.core.config import get_settings
from app.core.enums.enums import StatusRole

settings = get_settings()
logger = logging.getLogger(__name__)

class LoginService:
    @staticmethod
    async def login_user(db: Session, login_data: LoginDTO, response: Response) -> TokenResponseDTO:
        """Authenticate user and generate tokens"""
        user = await LoginService._authenticate_user(db, login_data)
        return await LoginService._handle_successful_login(user, response)

    @staticmethod
    async def _authenticate_user(db: Session, login_data: LoginDTO) -> User:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user or not verify_password(login_data.password, user.password):
            raise AuthenticationError("Incorrect email or password")
            
        if user.is_active == StatusRole.INACTIVE:
            raise AuthenticationError("User account is inactive")
            
        return user

    @staticmethod
    async def _handle_successful_login(user: User, response: Response) -> TokenResponseDTO:
        """Handle successful login by setting tokens"""
        # Dados do usuário para os tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "tenant_id": user.tenant_id,
            "role": user.role.value
        }
        
        # Create tokens
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)
        
        # Set cookies
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        
        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
