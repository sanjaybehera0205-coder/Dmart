from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.core.security import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Allow public routes
        public_paths = ["/login", "/register", "/forgot-password", "/reset-password"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Get token from header
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized: No token provided")

        # Remove "Bearer " prefix if exists
        if token.startswith("Bearer "):
            token = token[7:]

        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

        # Optionally, attach user info to request state
        request.state.user = payload

        return await call_next(request)
