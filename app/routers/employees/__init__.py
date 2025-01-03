# backend/app/routers/salons/__init__.py
from fastapi import APIRouter

from app.routers.employees.routes import crud


router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

router.include_router(crud.router)

