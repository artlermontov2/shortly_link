from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.users.router import login, register_user, logout
from app.reduction.router import shorten


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/index")
async def login(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        context={"request": request}
    )

@router.get("/shorten_url")
async def shorten(request: Request):
    return templates.TemplateResponse(
        name="shorten.html",
        context={"request": request}
    )

@router.get("/user_register")
async def register(request: Request):
    return templates.TemplateResponse(
        name="register.html",
        context={"request": request}
    )