# app/routers/ratings/__init__.py
from fastapi import APIRouter

from .routes import employees

router = APIRouter(prefix="/employees", tags=["employees"])
router.include_router(employees.router)
