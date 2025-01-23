# app/routers/offering/__init__.py
from fastapi import APIRouter
from .routes import crud

router = APIRouter(prefix="/salons/{salon_id}/offering", tags=["Offering-Salon-Service"])
router.include_router(crud.router)
