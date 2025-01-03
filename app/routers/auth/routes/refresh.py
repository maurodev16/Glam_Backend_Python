# backend/app/routers/auth/routes/refresh.py
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import logging
from app.models import user_model
from app.core.security.refresh_token import create_refresh_token, decode_refresh_token
from app.core.security.jwt import create_access_token
from ....core.database import get_db
from ....core.config import get_settings
settings = get_settings()
# Configure logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/refresh")
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    try:
        # Decodificar refresh token
        payload = decode_refresh_token(refresh_token)
        user_id = payload.get("sub")
        
        # Buscar usuário
        user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Criar novos tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "tenant_id": user.tenant_id,
            "role": user.role.value
        }
        
        new_access_token = create_access_token(data=token_data)
        new_refresh_token = create_refresh_token(data=token_data)
        
        # Atualizar cookies
        response.set_cookie(
            key="access_token",
            value=f"Bearer {new_access_token}",
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
            max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="lax",
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token"
        )