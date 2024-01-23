from jose import jwt
import os
from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from app.users.dao import UserDAO

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashes_password) -> bool:
    return pwd_context.verify(plain_password, hashes_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
    )
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_user(email=email)
    if not user or not verify_password(password, user.password):
        return None
    return user