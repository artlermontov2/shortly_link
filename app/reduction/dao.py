from datetime import date
from sqlalchemy import insert, select, and_
from app.database import async_session_maker
from app.reduction.models import ShortenModel


class ReductionDAO:
    model = ShortenModel

    @classmethod
    async def find_original_url(cls, token: str, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.long_url).where(
                and_(
                    cls.model.token == token,
                    cls.model.user_id == user_id
                )
            )
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def add(
            cls, long_url: str,
            user_id: int,
            token: str,
            creared_at: date,
            expiry_at: date
    ):
        async with async_session_maker() as session:
            query = insert(cls.model).values(
                long_url = long_url,
                user_id = user_id,
                token = token,
                creared_at = creared_at,
                expiry_at = expiry_at
            ).returning(ShortenModel)

            result = await session.execute(query)
            await session.commit()
            return result.scalar()
        
    @classmethod
    async def find_token(cls, long_url: str, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.token).where(
                and_(
                    cls.model.long_url == long_url,
                    cls.model.user_id == user_id
                )
            )
            result = await session.execute(query)
            return result.scalar()
        
