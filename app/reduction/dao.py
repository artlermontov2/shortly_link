from datetime import date, datetime

from fastapi_cache.decorator import cache
from sqlalchemy import and_, delete, desc, func, insert, select
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.reduction.models import ShortenModel
from app.logger import logger


class ReductionDAO:
    model = ShortenModel

    # Нужно заккоментировать кэш на время тестирования
    @classmethod
    @cache(expire=86400*30) # Кэш на 30 дней
    async def find_original_url(cls, token: str):
        async with async_session_maker() as session:
            query = select(cls.model.long_url).where(
                cls.model.token == token
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
        try:
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
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot add url"
            extra = {
                "long_url": long_url,
                "user_id": user_id,
                "token": token,
                "created_at": created_at,
                "expiry_at": expiry_at,
            }
            logger.error(msg, extra=extra, exc_info=True)
        
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

        

        
