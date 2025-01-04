# app/routers/commission/__init__.py
from fastapi import APIRouter
from .routes import crud

router = APIRouter(prefix="/commissions", tags=["commissions"])
router.include_router(crud.router)

__all__ = ['router']
