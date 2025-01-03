# backend/app/routers/auth/__init__.py
from fastapi import APIRouter

from app.routers.auth.routes import login, register, logout, me, refresh



router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        401: {"description": "Authentication failed"},
        403: {"description": "Forbidden"},
        404: {"description": "Resource not found"}
    }
)

router.include_router(login.router)
router.include_router(logout.router)
router.include_router(me.router)
router.include_router(refresh.router)
router.include_router(register.router)
