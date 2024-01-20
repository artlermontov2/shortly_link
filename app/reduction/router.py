from datetime import datetime, timedelta
from fastapi import APIRouter, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from hashids import Hashids
from app.reduction.schemas import UrlItem
from app.reduction.dao import ReductionDAO


router = APIRouter(
    tags=["Shortly Link"]
)

domain = 'http://127.0.0.1:8000'


def generate_token(url: str):
    hashids = Hashids(salt=url, min_length=7)
    token = hashids.encrypt(123)
    return token

@router.post("/shorten")
async def shorten(url: UrlItem):
    exists_token = await ReductionDAO.find_token(long_url=url.long_url, user_id=1)
    if exists_token:
        short_url = f'{domain}/{exists_token}'
        return {"msg": "The link for this address already exists", "short_url": short_url}
    token = generate_token(url.long_url)
    short_url = f'{domain}/{token}'
    await ReductionDAO.add(
        long_url=url.long_url,
        user_id=1,
        token=token,
        creared_at=datetime.now(),
        expiry_at=datetime.now() + timedelta(days=1)
    )
    return {"msg": "A short link has been created", "short_url": short_url}

@router.get("/{short_url}")
async def redirect_to_original_url(short_url: str):
    long_url = await ReductionDAO.find_original_url(token=short_url, user_id=1)

    if long_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Original URL not found'
        )
    return RedirectResponse(url=long_url)
