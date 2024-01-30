from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


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