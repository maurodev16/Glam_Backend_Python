# backend/app/routers/salons/__init__.py
from fastapi import APIRouter

from app.routers.salons.routes import crud


router = APIRouter(
    prefix="/salons",
    tags=["salons"]
)

router.include_router(crud.router)

