from contextvars import ContextVar
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from app.core.security.jwt import decode_token
import logging

logger = logging.getLogger(__name__)

# Context variables
tenant_id: ContextVar[str] = ContextVar("tenant_id", default=None)
user_id: ContextVar[str] = ContextVar("user_id", default=None)

class TenantMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
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
        """Check if the current path should be excluded from tenant validation."""
        return any(path.startswith(excluded) for excluded in self.excluded_paths)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            # Skip middleware for excluded paths
            if self.is_path_excluded(request.url.path):
                return await call_next(request)

            # Get the authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                logger.warning("Missing or invalid Authorization header")
                return await call_next(request)

            # Extract token and decode it
            token = auth_header.split(" ")[1]
            try:
                payload = decode_token(token)
                tenant = payload.get("tenant_id")
                user = payload.get("user_id")

                # Set context variables
                if tenant:
                    tenant_id.set(tenant)
                if user:
                    user_id.set(user)

                # Optionally store in request.state
                request.state.tenant_id = tenant
                request.state.user_id = user
            except Exception as e:
                logger.error(f"Token validation error: {str(e)}")
                # Allow the request to continue, but without tenant/user context
                pass

            logger.debug(f"Tenant ID: {tenant_id.get()}, User ID: {user_id.get()}")

            return await call_next(request)

        except Exception as e:
            logger.error(f"Middleware error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500, detail="Internal Server Error"
            )
