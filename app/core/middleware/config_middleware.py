from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware.tenant_middleware import TenantMiddleware
from app.core.config import get_settings

settings = get_settings()

def configure_middlewares(app: FastAPI) -> None:
    # Configuração de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Adiciona TenantMiddleware
    app.add_middleware(TenantMiddleware)
