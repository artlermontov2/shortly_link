import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import Depends, Request
from jose import JWTError, jwt

from app.exeptions import (
    IncorrectTokenFormatExeption,
    TokenAbsentExeption,
    TokenExpiredExeption,
    UserIsNotPresentExeption,
)
from app.users.dao import UserDAO

load_dotenv()

# получаем токен cookie
def get_token(request: Request):
    token = request.cookies.get("web-app-session-id")

    if not token:
        raise TokenAbsentExeption
    return token

# достаём юзера из cookie
async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM") 
        )
    except JWTError:
        raise IncorrectTokenFormatExeption
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredExeption
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentExeption
    
    user = await UserDAO.find_by_id(id=int(user_id))
    if not user:
        raise UserIsNotPresentExeption
    
    return user

    