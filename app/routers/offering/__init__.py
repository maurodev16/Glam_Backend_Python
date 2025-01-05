# app/routers/offering/__init__.py
from fastapi import APIRouter


from .routes import offering_routes

router = APIRouter(prefix="/offering", tags=["offering"])
router.include_router(offering_routes.router)
