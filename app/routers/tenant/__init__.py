from fastapi import APIRouter
from .routes import crud, admin_routes

router = APIRouter(prefix="/admin/tenants", tags=["admin"])
router.include_router(crud.router)
router.include_router(admin_routes.router)


__all__ = ['router']
