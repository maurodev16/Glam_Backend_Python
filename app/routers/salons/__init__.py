# app/routers/salons/__init__.py
from fastapi import APIRouter
from .routes import crud

router = APIRouter(prefix="/salons", tags=["salons"])
router.include_router(crud.router)
