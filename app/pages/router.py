from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.users.models import UsersModel
from app.users.dependencies import get_current_user
from app.users.router import get_my_all_urls


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
async def shorten(
    request: Request, 
    user: UsersModel = Depends(get_current_user),
):
    return templates.TemplateResponse(
        name="shorten.html",
        context={"request": request, "user": user}
    )

@router.get("/user_register")
async def register(request: Request):
    return templates.TemplateResponse(
        name="register.html",
        context={"request": request}
    )

@router.get("/user_link")
async def register(
    request: Request,
    user_links=Depends(get_my_all_urls), 
    user: UsersModel = Depends(get_current_user),
):
    return templates.TemplateResponse(
        name="user.html",
        context={"request": request, "user_links": user_links, "user": user}
    )