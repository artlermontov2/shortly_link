import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("url,status_code", [
    ("https://aminalaee.dev/sqladmin/working_with_files/", 200),
    ("https://github.com/long2ice/fastapi-cache/issues/49", 200),
    (123, 422),
])
async def test_add_url(auth_ac: AsyncClient, url, status_code):
    responce = await auth_ac.post("/shorten", json={
        "long_url": url
    })

    assert responce.status_code == status_code


@pytest.mark.parametrize("token,status_code", [
    ("zc4pAiE", 307),
    ("ocEkjik", 307),
    ("qwe", 404),
])
async def test_redirect_to_origin_url(auth_ac: AsyncClient, token, status_code):
    responce = await auth_ac.get(f"{token}")
    assert responce.status_code == status_code