import pytest

@pytest.mark.asyncio
async def test_user_registration_and_login(client):
    register_data = {
        "name": "Test User",
        "login": "testuser",
        "password": "testpass123"
    }
    res = await client.post("/users/register", json=register_data)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

    res = await client.post("/users/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    token = data["access_token"]
    assert token.startswith("ey")

    res = await client.post("/users/login", data={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert res.status_code == 401

    res = await client.post("/users/register", json=register_data)
    assert res.status_code == 400
