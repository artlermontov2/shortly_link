from fastapi import APIRouter, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from hashids import Hashids
from app.reduction.schemas import UrlItem


router = APIRouter(
    tags=['Shortly Link']
)


def generate_short_url(url: str):
    hashids = Hashids(salt=url, min_length=7)
    token = hashids.encrypt(123)
    return token

# Достаём из БД длинный url
def get_long_url(short_url: str):
    long_url = 'https://habr.com/ru/companies/spectr/articles/715290/'
    return long_url

@router.post("/shorten")
async def shorten(url: UrlItem):
    token = generate_short_url(url.long_url)
    short_url = f'https://test.com/{token}'
    return {"short_url": short_url, 'long_url': url.long_url, 'token': token}

@router.get("/")
async def redirect_to_original_url(short_url: str):
    long_url = get_long_url(short_url)
    if long_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Original URL not found'
        )
    return RedirectResponse(url=long_url)
