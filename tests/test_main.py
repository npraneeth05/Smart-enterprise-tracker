import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.storage import storage

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    """Clear memory storage before each test execution."""
    storage.clear()
    yield


def test_add_expense():
    payload = {
        "title": "Coffee",
        "amount": 4.50,
        "category": "Food",
        "date": "2026-07-31",
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Coffee"
    assert data["amount"] == 4.50
    assert data["category"] == "Food"


def test_view_all_and_filter():
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 15.00,
            "category": "Food",
            "date": "2026-07-31",
        },
    )
    client.post(
        "/expenses",
        json={
            "title": "Bus Pass",
            "amount": 50.00,
            "category": "Transport",
            "date": "2026-07-31",
        },
    )

    # Get all
    res_all = client.get("/expenses")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 2

    # Filter by category
    res_food = client.get("/expenses?category=food")
    assert res_food.status_code == 200
    assert len(res_food.json()) == 1
    assert res_food.json()[0]["category"] == "Food"


def test_calculate_totals():
    client.post(
        "/expenses",
        json={"title": "Dinner", "amount": 30.00, "category": "Food"},
    )
    client.post(
        "/expenses",
        json={"title": "Snack", "amount": 10.00, "category": "Food"},
    )
    client.post(
        "/expenses",
        json={"title": "Movie", "amount": 15.00, "category": "Entertainment"},
    )

    res = client.get("/expenses/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_expenses"] == 55.00
    assert data["category_totals"]["Food"] == 40.00
    assert data["category_totals"]["Entertainment"] == 15.00


def test_delete_expense():
    res = client.post(
        "/expenses",
        json={"title": "Taxi", "amount": 20.00, "category": "Transport"},
    )
    expense_id = res.json()["id"]

    # Delete existing
    del_res = client.delete(f"/expenses/{expense_id}")
    assert del_res.status_code == 204

    # Verify deletion
    all_res = client.get("/expenses")
    assert len(all_res.json()) == 0

    # Delete non-existent
    del_res_404 = client.delete("/expenses/invalid-id")
    assert del_res_404.status_code == 404
