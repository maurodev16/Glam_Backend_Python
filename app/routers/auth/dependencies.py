# backend/app/routers/auth/dependencies.py
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from app.core.enums.enums import StatusRole
from app.core.security.jwt import decode_token
from ...core.database import get_db
from ...models import user_model as models
from .exceptions import AuthenticationError
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="JWT")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    try:
        # Decode and verify token
        payload = decode_token(token)
        logger.debug(f"Token decoded successfully. Payload: {payload}")
        
        user_id = payload.get("sub")
        
        if not user_id or not str(user_id).isdigit():
            logger.error("Invalid 'sub' claim in token")
            raise AuthenticationError("Invalid token: 'sub' claim must be an integer")

        # Make tenant_id optional since it might not be required for all users
        user_id = int(user_id)
        tenant_id = payload.get("tenant_id")

        # Build query based on available data
        query = db.query(models.User).filter(models.User.id == user_id)
        
        if tenant_id is not None:
            query = query.filter(models.User.tenant_id == tenant_id)

        user = query.first()
        logger.debug(f"User found in database: {user is not None}")

        if not user:
            raise AuthenticationError("User not found")

        if user.is_active == StatusRole.INACTIVE:
            raise AuthenticationError("User account is inactive")

        logger.debug("Authentication successful")
        return user
    
    except JWTError as jwt_err:
        logger.error(f"JWT decoding error: {str(jwt_err)}")
        raise AuthenticationError("Invalid or expired token")
    
    except SQLAlchemyError as db_err:
        logger.error(f"Database error: {str(db_err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {str(e)}")
        raise AuthenticationError("Authentication failed")