# core/middleware.py
from fastapi.middleware.cors import CORSMiddleware
from ..config import get_settings
settings = get_settings()

def configure_middleware(app):
    # Determine as origens permitidas com base no ambiente
    allowed_origins = settings.cors_origins or ["*"]  # Use `*` se nenhuma origem for definida

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,  # Permitir envio de cookies e headers de autenticação
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Métodos HTTP permitidos
        allow_headers=["Authorization", "Content-Type", "Accept", "X-CSRF-Token"],  # Headers permitidos
        expose_headers=["Content-Length", "X-Custom-Header"],  # Headers que o cliente pode acessar
        max_age=600,  # Tempo em segundos para armazenar em cache a resposta do CORS
    )