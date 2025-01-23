# backend/app/routers/users/__init__.py
from fastapi import APIRouter

from app.routers.users.routes import crud, profile, status, upgrade


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={401: {"description": "Not authenticated"}}
)

router.include_router(crud.router)
router.include_router(profile.router)
router.include_router(status.router)
router.include_router(upgrade.router)
