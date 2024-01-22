from datetime import date
from sqlalchemy import insert, delete, select
from app.database import async_session_maker
from app.users.models import UsersModel


class UserDAO:
    model = UsersModel

    @classmethod
    async def add_new_user(
        cls,
        password: str,
        email: str,
        created_at: date
    ):
        async with async_session_maker() as session:
            query = insert(cls.model).values(
                password=password,
                email=email,
                created_at=created_at
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == user_id)
            await session.execute(query)
            await session.commit()

    @classmethod 
    async def find_user(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                cls.model.email == email
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod 
    async def find_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                cls.model.id == id
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
