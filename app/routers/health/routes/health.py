from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text  
from app.core.database import get_db
from app.core.config import get_settings
settings = get_settings()
import logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "origin": settings.ALLOWED_ORIGINS,
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "environment": settings.ENVIRONMENT,
            "origin": settings.ALLOWED_ORIGINS,
            "database": "disconnected",
            "error": str(e)
        }
