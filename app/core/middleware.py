# core/middleware.py
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
settings = get_settings()

def configure_middleware(app):
    if settings.is_production:
        allowed_origins = settings.cors_origins
    else:
        allowed_origins = ["http://localhost:6060"]  # Permite localhost para desenvolvimento
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["Content-Length"],
        max_age=600,
    )
