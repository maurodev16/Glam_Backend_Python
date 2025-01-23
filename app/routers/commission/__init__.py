# app/routers/commission/__init__.py
from fastapi import APIRouter
from .routes import crud


router = APIRouter(
    prefix="/salons/{salon_id}/employees/{employee_id}/commissions",
    tags=["Employee-Commissions"]
)
router.include_router(crud.router)

__all__ = ['router']
