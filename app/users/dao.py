from datetime import date, datetime
from sqlalchemy import insert, select, and_, event, delete
from app.database import async_session_maker
from pydantic import BaseModel
from app.users.schemas import SUser
from app.users.models import UsersModel


class UserDAO(BaseModel):
    model = UsersModel

    @classmethod
    async def add_new_user(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == user_id)
            await session.execute(query)
            await session.commit()
