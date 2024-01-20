from datetime import date
from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    password: str
    email: EmailStr
    creared_at: date