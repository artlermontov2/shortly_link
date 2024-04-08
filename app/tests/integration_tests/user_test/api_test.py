import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,created_at,status_code", [
    ("markus@test.ru", "test", "2024-02-12", 201),
    ("markus@test.ru", "tost", "2024-02-12", 409),
    ("markus", "tost", "2024-02-12", 422),
])                       
async def test_register_user(
    ac: AsyncClient,
    email, password, created_at, status_code
):
    responce = await ac.post(
        "api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "created_at": created_at
        }
    )

    assert responce.status_code == status_code


@pytest.mark.parametrize("email,password,created_at,status_code", [
    ("artem@test.com", "test", "2024-02-12", 200),
    ("wrong@person.com", "test", "2024-02-12", 401),
    ("artem", "test", "2024-02-12", 422),
])
async def test_login(
    ac: AsyncClient,
    email, password, created_at, status_code
):
    responce = await ac.post(
        "api/v1/auth/login",
        json={
            "email": email,
            "password": password,
            "created_at": created_at
        }
    )

    assert responce.status_code == status_code