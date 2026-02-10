from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request}
    )

@router.get("/dashboard")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@router.get("/users")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {"request": request}
    )
@router.get("/cart")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "cart.html",
        {"request": request}
    )
@router.get("/order")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "order.html",
        {"request": request}
    )
@router.get("/profile")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request}
    )
@router.get("/settings")
def signup_page(request: Request):
    return templates.TemplateResponse(
        "settings.html",
        {"request": request}
    )