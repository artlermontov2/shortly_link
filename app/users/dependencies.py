import os
from datetime import datetime
from fastapi import Depends, Request
from dotenv import load_dotenv
from jose import jwt, JWTError
from app.users.dao import UserDAO
from app.exeptions import (
    TokenAbsentExeption, IncorrectTokenFormatExeption,
    TokenExpiredExeption, UserIsNotPresentExeption,
)


load_dotenv()

# получаем токен cookie
def get_token(request: Request):
    token = request.cookies.get("web-app-session-id")
    print(token)

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
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredExeption
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentExeption
    
    user = await UserDAO.find_by_id(id=int(user_id))
    if not user:
        raise UserIsNotPresentExeption
    
    return user

    