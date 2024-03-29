import asyncio
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from pytest_asyncio import is_async_test
import pytest
from sqlalchemy import insert

from app.database import Base, async_session_maker, engine
from app.users.models import UsersModel
from app.reduction.models import ShortenModel
from app.main import app as fastapi_app

from fastapi.testclient import TestClient
from httpx import AsyncClient


load_dotenv()

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert os.getenv("MODE") == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_model_mock(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)
        
    users = open_model_mock("users")
    urls = open_model_mock("urls")

    for user in users:
    # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
        user["created_at"] = datetime.strptime(user["created_at"], "%Y-%m-%d")

    for url in urls:
        url["created_at"] = datetime.strptime(url["created_at"], "%Y-%m-%d")
        url["expiry_at"] = datetime.strptime(url["expiry_at"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_users = insert(UsersModel).values(users)
        add_urls = insert(ShortenModel).values(urls)

        await session.execute(add_users)
        await session.execute(add_urls)

        await session.commit()


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker)


@pytest.fixture(scope="function")   
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")   
async def auth_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "artem@test.com",
            "password": "test",
            "created_at": "2024-02-12"
        })
        assert ac.cookies["web-app-session-id"]
        yield ac


# @pytest.fixture(scope="function")
# async def session():
#     async with async_session_maker as session:
#         yield session
        
# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


        