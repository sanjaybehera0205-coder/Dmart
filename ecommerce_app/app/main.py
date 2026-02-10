from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import auth_routes, product_routes, user_routes, routes

app = FastAPI(title="E-Commerce API")

# Static files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML Pages
app.include_router(routes.router, tags=["Pages"])

# API Routes
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
