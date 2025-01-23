# app/routers/business-hours/__init__.py
from fastapi import APIRouter

from .routes import holiday_crud

# Router principal
router = APIRouter(prefix="/salons/{salon_id}/holidays", tags=["Business-Holidays"])

# Incluir os sub-routers
router.include_router(holiday_crud.router)

__all__ = ['router']
