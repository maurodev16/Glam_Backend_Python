from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.core.middleware import configure_middleware
from app.core.database import engine, Base, get_db
import logging

# Import dos routers
from app.routers import auth_router, health_router, salons_router # All Routers 

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
    
    # Configura middleware
    configure_middleware(app)
    
    # Inclui todos os routers
    app.include_router(health_router.router)
    app.include_router(auth_router.router)
    app.include_router(salons_router.router)

    
    @app.on_event("startup")
    async def startup_event():
        logger.info("API started successfully")
        # Opcional: criar tabelas do banco de dados durante o startup
        Base.metadata.create_all(bind=engine)
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("API shutdown")
    
    return app

app = create_application()