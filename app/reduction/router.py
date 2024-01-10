from fastapi import APIRouter


router = APIRouter(
    tags=['Shortly Link']
)


def generate_short_url():
    pass

def get_long_url():
    pass

@router.post("/shorten")
async def shorten():
    return {"result": 'Test'}

@router.get("/{short_url}")
async def redirect_to_original_url():
    pass