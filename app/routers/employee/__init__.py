# app/routers/ratings/__init__.py
from fastapi import APIRouter

from .routes import crud

router = APIRouter(prefix="/salons/{salon_id}/employees", tags=["Employees"])
router.include_router(crud.router)
