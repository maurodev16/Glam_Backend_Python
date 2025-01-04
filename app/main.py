# main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.middleware.middleware_config import configure_middlewares
from app.routers import health, users, salons, auth, commission
import logging

from app.core.middleware.tenant_middleware import TenantMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    app = FastAPI(
        title="Salon API",
        version="1.0.0",
        description="API for salon management",
    )
    
    # Configure middlewares
    configure_middlewares(app)
    app.add_middleware(TenantMiddleware)
    
    # Inclui todos os routers
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(salons.router)
    app.include_router(commission.router)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("API started successfully")
        Base.metadata.create_all(bind=engine)
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("API shutdown")
    
    return app

app = create_application()
