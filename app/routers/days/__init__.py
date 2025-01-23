# app/routers/business-hours/__init__.py
from fastapi import APIRouter
from .routes import  days_crud

# Router principal
router = APIRouter(prefix="/days-of-week", tags=["Business-Days-of-Week"])

# Incluir os sub-routers
router.include_router(days_crud.router )

__all__ = ['router']
