# app/core/middleware/tenant_middleware.py
from contextvars import ContextVar
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.requests import Request
from starlette.datastructures import Headers
from app.core.security.jwt import decode_token
import logging

logger = logging.getLogger(__name__)
tenant_id: ContextVar[str] = ContextVar("tenant_id", default=None)
user_id: ContextVar[str] = ContextVar("user_id", default=None)
class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.app = app
        
        # async def __call__(self, scope, receive, send):
        #     headers = Headers(scope=scope)
        #     maybe_tenant_id = headers.get("X-Tenant-Id")
        #     maybe_set_context(maybe_tenant_id, tenant_id)
        #     request = Request(scope)
        #     token = request.cookies.get("access_token")
        #     maybe_user_id = get_user_id_from_valid_token(token)
        #     logger.debug(f"Maybe user ID: {maybe_user_id}")
        #     maybe_set_context(maybe_user_id, user_id)
        #     logger.debug(f"Tenant ID: {tenant_id.get()}, User ID: {user_id.get()}")
        #     await self.app(scope, receive, send)
            
            
            
        # Define excluded paths as a tuple for better performance
        self.excluded_paths = (
            "/auth/login",
            "/auth/register",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/users/upgrade-to-business"
        )

    def is_path_excluded(self, path: str) -> bool:
        """Check if the current path should be excluded from tenant validation"""
        return any(path.startswith(excluded) for excluded in self.excluded_paths)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            # Skip middleware for excluded paths
            if self.is_path_excluded(request.url.path):
                return await call_next(request)

            # Get authorization header
            auth_header = request.headers.get("Authorization")
            
            # If no auth header is present, allow the request to continue
            # The route's dependencies will handle authentication if needed
            if not auth_header:
                return await call_next(request)

            # Validate token format
            if not auth_header.startswith("Bearer "):
                logger.warning("Invalid authorization header format")
                return await call_next(request)

            # Extract and validate token
            token = auth_header.split(" ")[1]
            if token:
                try:
                    payload = decode_token(token)
                    # Store tenant information in request state if needed
                    request.state.tenant_id = payload.get("tenant_id")
                except Exception as e:
                    logger.error(f"Token validation error: {str(e)}")
                    # Let the request continue - route dependencies will handle auth
                    pass

            return await call_next(request)

        except Exception as e:
            logger.error(f"Middleware error: {str(e)}", exc_info=True)
            raise
