from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.initialize import initialize
from app.routes import (auth_routes,product_routes,user_routes,routes,cart_routes,order_routes)
from app.shared.middleware.auth_middleware import AuthMiddleware

from app.shared.middleware.logging_middleware import LoggingMiddleware
# from app.middleware.rate_limit_middleware import RateLimitMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    initialize("app/config/app.properties")
    yield
    # Shutdown logic (if needed)
    print("Application shutting down...")

app = FastAPI(
    title="E-Commerce API",
    lifespan=lifespan
)

#  Add Middleware (ORDER MATTERS)
app.add_middleware(LoggingMiddleware)
# app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)

# Include Routers
app.include_router(routes.router, tags=["App"])
app.include_router(auth_routes.router, tags=["Auth"])
app.include_router(product_routes.router, tags=["Products"])
app.include_router(user_routes.router, tags=["Users"])
app.include_router(cart_routes.router, tags=["Add to Cart"])
app.include_router(order_routes.router, tags=["Order Details"])
