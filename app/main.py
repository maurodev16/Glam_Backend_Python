from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.middleware.config_middleware import configure_middlewares
from app.routers import health, tenant, auth, users, salons, business_schedule, commission, employee, offering, ratings
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
    app.include_router(tenant.router)
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(salons.router)
    app.include_router(employee.router)
    app.include_router(offering.router)
    app.include_router(ratings.router)
    app.include_router(business_schedule.router)
    app.include_router(commission.router)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("API started successfully")
        try:
            # Criar todas as tabelas se não existirem
            logger.info("Creating tables in the database...")
            #Base.metadata.drop_all(bind=engine)
            #logger.info("Tables Droped successfully.")
            Base.metadata.create_all(bind=engine)
            logger.info("Tables created successfully.")
        except Exception as e:
            logger.error(f"Error while creating tables: {e}")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("API shutdown")
    
    return app

app = create_application()
