import pytest


async def create_receipt(client, headers) -> int:
    receipt_data = {
        "products": [
            {"name": "Product A", "price": 100.0, "quantity": 2},
            {"name": "Product B", "price": 50.0, "quantity": 1.5}
        ],
        "payment": {
            "type": "cash",
            "amount": 300.0
        }
    }

    res = await client.post("/receipts/", json=receipt_data, headers=headers)
    assert res.status_code == 200
    data = res.json()

    expected_total = 100.0 * 2 + 50.0 * 1.5
    assert data["total"] == pytest.approx(expected_total, rel=1e-2)
    assert data["rest"] == pytest.approx(300.0 - expected_total, rel=1e-2)

    return data["id"]


@pytest.mark.asyncio
async def test_create_and_get_receipt(client, registered_user):
    headers = registered_user["headers"]

    # Створення чеку
    receipt_id = await create_receipt(client, headers)

    # Перевірка списку чеків
    res = await client.get("/receipts/", headers=headers)
    assert res.status_code == 200
    receipts = res.json()
    assert any(r["id"] == receipt_id for r in receipts)

    # Перевірка одного чеку
    res = await client.get(f"/receipts/{receipt_id}", headers=headers)
    assert res.status_code == 200
    detailed = res.json()
    assert detailed["id"] == receipt_id
    assert len(detailed["products"]) == 2
