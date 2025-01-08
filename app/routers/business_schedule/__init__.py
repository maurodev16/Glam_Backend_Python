# app/routers/business-hours/__init__.py
from fastapi import APIRouter
from .routes import crud

router = APIRouter(prefix="/salons/{salon_id}/business-hours", tags=["business-hours"])
router.include_router(crud.router)

__all__ = ['router']
