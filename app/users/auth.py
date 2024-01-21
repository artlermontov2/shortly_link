from jose import jwt
import os
from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.users.dao import UserDAO

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashes_password) -> bool:
    return pwd_context.verify(plain_password, hashes_password)