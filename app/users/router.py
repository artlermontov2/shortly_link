from datetime import datetime
from fastapi import APIRouter, Response, Depends
from app.users.schemas import SUser
from app.users.auth import get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SUser
from app.users.auth import authenticate_user, create_access_token
from app.exeptions import UserAlredyExistsException, IncorrectEmailOrPasswordException
from app.users.dependencies import get_current_user
from app.users.models import UsersModel



router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register")
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
    return {"msg": "Пользователь зарегистрирован!"}

@router.post("/login")
async def login(responce: Response, user_data: SUser):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    responce.set_cookie("web-app-session-id", access_token, httponly=True)
    print(access_token)
    return {"msg": f"Привет, {user.email}!"}

@router.post("/logout")
async def logout(responce: Response):
    responce.delete_cookie("web-app-session-id")
    return {"msg": "Вы вышли из системы"}

@router.get("/me")
async def get_user_me(current_user: UsersModel = Depends(get_current_user)):
    return current_user

# @router.get("/find_user/")
# async def find_user(email: EmailStr, password: str):
#     return await authenticate_user(email=email, password=password)