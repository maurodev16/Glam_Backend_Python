from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging
from .config import get_settings

# Obter as configurações do sistema
settings = get_settings()

# Configuração de logs
logging.basicConfig(level=logging.DEBUG if settings.is_development else logging.INFO)
logger = logging.getLogger(__name__)

def create_database_engine():
    """Cria e configura a conexão com o banco de dados"""
    try:
        # Criar engine com configurações dinâmicas e desabilitar transações para DDL
        engine = create_engine(
            settings.get_database_url(),
            pool_pre_ping=True,
            poolclass=QueuePool,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            isolation_level='AUTOCOMMIT', # Importante: permite DDL fora de transações
            connect_args={'options': '-c search_path=public,nile'}
        )
        logger.info("Conexão com o banco de dados configurada com sucesso.")
        return engine
    except exc.SQLAlchemyError as e:
        logger.error(f"Erro ao configurar conexão com o banco de dados: {e}")
        raise

# Criar o engine de conexão com base nas configurações
engine = create_database_engine()

# Configurar o SessionLocal para gerenciar sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definição dos modelos
Base = declarative_base()

def get_db():
    """
    Gerenciador de contexto para obter e gerenciar a sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    except exc.SQLAlchemyError as e:
        logger.error(f"Erro durante o acesso ao banco de dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()