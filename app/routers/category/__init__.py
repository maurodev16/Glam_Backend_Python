# app/routers/commission/__init__.py
from fastapi import APIRouter
from .routes import crud


router = APIRouter(
    prefix="/salons/{salon_id}/category",
    tags=["Type-Of-Categories"]
)
router.include_router(crud.router)

__all__ = ['router']
