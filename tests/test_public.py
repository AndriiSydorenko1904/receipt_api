import pytest


async def create_receipt(client, headers) -> int:
    receipt_data = {
        "products": [
            {"name": "Drone A", "price": 150000.0, "quantity": 1},
            {"name": "Battery Pack", "price": 31000.0, "quantity": 2}
        ],
        "payment": {
            "type": "card",
            "amount": 250000.0
        }
    }

    res = await client.post("/receipts/", json=receipt_data, headers=headers)
    assert res.status_code == 200
    return res.json()["id"]


@pytest.mark.asyncio
async def test_public_receipt_view(client, registered_user):
    headers = registered_user["headers"]

    # Створення чеку
    receipt_id = await create_receipt(client, headers)

    # Публічний перегляд у текстовому форматі
    res = await client.get(f"/receipts/public/{receipt_id}?format=text")
    assert res.status_code == 200
    text = res.text
    assert "Дякуємо за покупку" in text
    assert "Drone A" in text
    assert "Battery Pack" in text

    # Публічний перегляд у форматі JSON
    res = await client.get(f"/receipts/public/{receipt_id}?format=json")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["id"] == receipt_id
    assert len(json_data["products"]) == 2
