# app/routers/salons/__init__.py
from fastapi import APIRouter
from .routes import crud, services, ratings, employees

router = APIRouter(prefix="/salons", tags=["salons"])
router.include_router(crud.router)
router.include_router(services.router)
router.include_router(ratings.router)
router.include_router(employees.router)
