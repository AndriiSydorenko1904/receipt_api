import uuid
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.core.database import get_db
from tests.test_database import get_test_db, init_test_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_db():
    await init_test_db()


@pytest_asyncio.fixture
async def override_get_db():
    async for session in get_test_db():
        yield session


@pytest_asyncio.fixture
async def client(override_get_db):
    app.dependency_overrides[get_db] = lambda: override_get_db
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def registered_user(client):
    login = f"user_{uuid.uuid4().hex[:8]}"
    password = "testpass123"

    register_data = {
        "name": "Test User",
        "login": login,
        "password": password,
    }

    res = await client.post("/users/register", json=register_data)
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    return {
        "token": token,
        "headers": headers,
        "login": login,
        "password": password,
    }
