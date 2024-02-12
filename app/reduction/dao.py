from datetime import date, datetime
from sqlalchemy import desc, insert, select, and_, delete, func
from sqlalchemy.orm import load_only
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
            created_at: date,
            expiry_at: date
    ):
        async with async_session_maker() as session:
            query = insert(cls.model).values(
                long_url = long_url,
                user_id = user_id,
                token = token,
                created_at = created_at,
                expiry_at = expiry_at
            ).returning(ShortenModel)

            result = await session.execute(query)
            await session.commit()
            return result.scalar()
        
    @classmethod
    async def find_users_token(cls, long_url: str, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.token).where(
                and_(
                    cls.model.long_url == long_url,
                    cls.model.user_id == user_id
                )
            )
            result = await session.execute(query)
            return result.scalar()
        
    @classmethod
    async def find_all_user_url(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                cls.model.user_id == user_id
            ).order_by(desc(cls.model.created_at))
            query = query.options(load_only(cls.model.token, cls.model.long_url))
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_all_user_url_pagination(
        cls, user_id: int, size: int, page: int
    ):
        offset = (page - 1) * size
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                cls.model.user_id == user_id
            ).order_by(desc(cls.model.created_at))
            
            query = query.options(
                load_only(cls.model.token, cls.model.long_url)
            ).limit(size).offset(offset)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def count_user_urls(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def find_token(cls, long_url: str):
        async with async_session_maker() as session:
            query = select(cls.model.token).where(
                cls.model.long_url == long_url
            )
            result = await session.execute(query)
            return result.scalar()
        
    @classmethod
    async def delete_after_expire(cls):
        async with async_session_maker() as session:
            query = delete(cls.model).where(
                cls.model.expiry_at <= datetime.now()
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

        

        
