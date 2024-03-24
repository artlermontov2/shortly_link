from datetime import datetime

from fastapi import APIRouter, Depends, Query, Response, status

from app.exeptions import IncorrectEmailOrPasswordException, UserAlredyExistsException
from app.reduction.dao import ReductionDAO
from app.reduction.router import domain
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import UsersModel
from app.users.schemas import SUser

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: SUser):
    existing_user = await UserDAO.find_user(email=user.email)
    if existing_user:
        raise UserAlredyExistsException
    
    hashed_password = get_password_hash(password=user.password)
    await UserDAO.add_new_user(
        password=hashed_password,
        email=user.email,
        created_at=datetime.now()
    )

@router.post("/login")
async def login(response: Response, user_data: SUser):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("web-app-session-id", access_token, httponly=True)

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("web-app-session-id")

@router.get("/my_all")
async def get_my_all_urls(
    user: UsersModel = Depends(get_current_user),
    page: int = Query(1, alias="page", description="Номер страницы"),
    size: int = Query(10, alias="size", description="Размер страницы"),
):
    result = await ReductionDAO.find_all_user_url_pagination(
        user_id=user.id, size=size, page=page
    )
    total_urls = await ReductionDAO.count_user_urls(user_id=user.id)
    users_url = []
    for i in result:
        users_url.append(
            {
                "short_url": f'{domain}/{i.token}',
                "long_url": i.long_url,
                "id": i.id,
            }
        )
    return {
        "user_urls": users_url,
        "total": total_urls,
        "page": page,
        "size": size,
    }


# @router.get("/my_all")
# async def get_my_all_urls(user: UsersModel = Depends(get_current_user)):
#     result = await ReductionDAO.find_all_user_url(user_id=user.id)
#     users_url = []
#     for i in result:
#         users_url.append(
#             {
#                 "short_url": f'{domain}/{i.token}',
#                 "long_url": i.long_url,
#                 "id": i.id
#             }
#         )
#     return users_url
