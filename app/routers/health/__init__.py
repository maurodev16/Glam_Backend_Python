# backend/app/routers/salons/__init__.py
from fastapi import APIRouter

from app.routers.health.routes import health

router = APIRouter(
    tags=["health"],
    responses={
        503: {"description": "Service Unavailable"}
    }
)


router.include_router(health.router)

