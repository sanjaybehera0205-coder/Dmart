from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import auth_routes, product_routes, user_routes, routes,cart_routes, order_routes

app = FastAPI(title="E-Commerce API")

# Static files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML Pages
app.include_router(routes.router, tags=["App"])

# API Routes
app.include_router(auth_routes.router, tags=["Auth"])
app.include_router(product_routes.router, tags=["Products"])
app.include_router(user_routes.router, tags=["Users"])
app.include_router(cart_routes.router, tags=["Add to Cart"])
app.include_router(order_routes.router, tags=["Order Details"])
