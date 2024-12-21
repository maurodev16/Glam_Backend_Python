# core/database.py
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging
from .config import get_settings
settings = get_settings()

logging.basicConfig(level=logging.INFO if settings.is_development else logging.INFO)
logger = logging.getLogger(__name__)

def create_database_engine():
    try:
        engine = create_engine(
            settings.get_database_url(),
            pool_pre_ping=True,
            poolclass=QueuePool,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
        )
        logger.info("Database connection configured successfully")
        return engine
    except exc.SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")
        raise

engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except exc.SQLAlchemyError as e:
        logger.error(f"Database access error: {e}")
        db.rollback()
        raise
    finally:
        db.close()