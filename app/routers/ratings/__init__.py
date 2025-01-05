# app/routers/ratings/__init__.py
from fastapi import APIRouter

from .routes import  ratings

router = APIRouter(prefix="/ratings", tags=["ratings"])
router.include_router(ratings.router)
