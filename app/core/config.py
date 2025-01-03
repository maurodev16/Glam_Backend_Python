# core/config.py
from pydantic_settings import BaseSettings
from typing import List
import json
from functools import lru_cache
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY_REFRESH: str 
    ENVIRONMENT: str = "development"  # valor padrão alterado para development
    ALLOWED_ORIGINS: str | List[str] = ["*"]  # valor padrão para desenvolvimento
    
    @property
    def is_development(self) -> bool:
        """Verifica se o ambiente é de desenvolvimento"""
        return self.ENVIRONMENT.lower() in ("development", "dev", "local")
    
    @property
    def is_production(self) -> bool:
        """Verifica se o ambiente é de produção"""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def cors_origins(self) -> List[str]:
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]  # Aceitar todas as origens (somente para desenvolvimento)
        """Processa as origens permitidas para CORS"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            try:
                # Tenta converter string JSON em lista
                return json.loads(self.ALLOWED_ORIGINS)
            except json.JSONDecodeError:
                # Se não for JSON válido, divide por vírgulas ou retorna como lista única
                return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")] if "," in self.ALLOWED_ORIGINS else [self.ALLOWED_ORIGINS]
        return self.ALLOWED_ORIGINS

    def get_database_url(self) -> str:
        """Retorna a URL do banco de dados apropriada para o ambiente"""
        if self.is_development:
            # Para ambiente de desenvolvimento, use uma URL local padrão
            return "postgresql://postgres:postgres@localhost:5432/scheduling_local_db"
        return self.DATABASE_URL

    class Config:
        # A variável 'env_file' vai ser dinâmica com base no valor do ENVIRONMENT
        env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Retorna uma instância cacheada das configurações"""
    return Settings()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'app.core.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}