# app/routers/business-hours/__init__.py
from fastapi import APIRouter

from .routes import hour_crud

# Router principal
router = APIRouter(prefix="/salons/{salon_id}/hours", tags=["Business-Hours"])

# Incluir os sub-routers
router.include_router(hour_crud.router)

__all__ = ['router']
