# app/core/middleware/middleware_config.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware.tenant_middleware import TenantMiddleware

def configure_middlewares(app: FastAPI) -> None:
    # Configura CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Adiciona TenantMiddleware
    app.add_middleware(TenantMiddleware)
