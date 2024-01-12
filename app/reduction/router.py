from fastapi import APIRouter
from hashids import Hashids


router = APIRouter(
    tags=['Shortly Link']
)


def generate_short_url(url: str):
    hashids = Hashids(salt=url, min_length=7)
    token = hashids.encrypt(123)
    return token

def get_long_url():
    pass

@router.post("/shorten")
async def shorten(url: str):
    token = generate_short_url(url)
    short_url = f'https://test.com/{token}'
    return {"short_url": short_url, 'long_url': url, 'token': token}

@router.get("/{short_url}")
async def redirect_to_original_url():
    pass
