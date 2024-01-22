from datetime import datetime, timedelta
from fastapi import APIRouter, Response, HTTPException, status
from app.users.schemas import SUser
from app.users.auth import get_password_hash
from app.users.dao import UserDAO



router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register/")
async def register_user(user: SUser):
    existing_user = await UserDAO.find_user(email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    
    hashed_password = get_password_hash(password=user.password)
    await UserDAO.add_new_user(
        password=hashed_password,
        email=user.email,
        created_at=datetime.now()
    )
    return {"msg": "Пользователь зарегистрирован!"}