import asyncio
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi_cache.decorator import cache
from hashids import Hashids

from app.reduction.schemas import UrlItem
from app.reduction.dao import ReductionDAO
from app.users.dependencies import get_current_user
from app.exeptions import OriginalUrlNotFound
from app.users.models import UsersModel 


router = APIRouter(
    tags=["Shortly Link"]
)

domain = 'http://127.0.0.1:8000'
expire_days = 30

def generate_token(url: str):
    hashids = Hashids(salt=url, min_length=7)
    token = hashids.encrypt(123)
    return token

@router.post("/shorten")
async def shorten(
    url: UrlItem, user: UsersModel = Depends(get_current_user)
):
    exists_token = await ReductionDAO.find_users_token(long_url=url.long_url, user_id=user.id)
    if exists_token:
        short_url = f'{domain}/{exists_token}'
        return {
            "msg": "Такая ссылка уже существует", "short_url": short_url
        }
    
    await ReductionDAO.delete_after_expire()
    token = generate_token(url.long_url)
    short_url = f'{domain}/{token}'
    await ReductionDAO.add(
        long_url=url.long_url,
        user_id=user.id,
        token=token,
        created_at=datetime.now(timezone.utc),
        expiry_at=datetime.now(timezone.utc) + timedelta(days=expire_days)
    )
    return {"msg": "Короткая ссылка была создана", "short_url": short_url}

@router.get("/{short_url}")
@cache(expire=20)
async def redirect_to_original_url(short_url: str):
    long_url = await ReductionDAO.find_original_url(token=short_url, user_id=1)
    if long_url is None:
        raise OriginalUrlNotFound
    return RedirectResponse(url=long_url)

@router.delete("/delete/{id}")
async def delete_record(id: int, user: UsersModel = Depends(get_current_user)):
    await ReductionDAO.delete(id=id, user_id=user.id)