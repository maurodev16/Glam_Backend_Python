# backend/app/routers/auth/routes/login.py
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
import logging
from app.core.enums.enums import StatusRole
from app.models import user_model
from app.core.security.jwt import create_access_token
from app.core.security.refresh_token import create_refresh_token
from app.dtos.auth.requests import LoginDTO
from app.services.auth.login_service import LoginService
from ....core.database import get_db
from ....core.security.password import verify_password
from ....core.config import get_settings
from ..exceptions import AuthenticationError
settings = get_settings()
# Configure logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/login")
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    try:
        # Converter OAuth2PasswordRequestForm para LoginDTO
        login_data = LoginDTO(
            email=form_data.username,
            password=form_data.password
        )
        
        # Usar o serviço de login
        login_service = LoginService()
        token_response = await login_service.login_user(
            db=db,
            login_data=login_data,
            response=response
        )
        
        return token_response
        
    except AuthenticationError as auth_error:
        logger.error(f"Authentication error: {str(auth_error)}")
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise AuthenticationError("Authentication failed")

