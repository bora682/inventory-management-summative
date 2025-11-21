import json

from app import app


def test_home_route():
    """Basic sanity check for the home route."""
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, dict)
        assert "message" in data


def test_get_inventory_route():
    """GET /inventory should return a list of items."""
    with app.test_client() as client:
        response = client.get("/inventory")
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, list)
        # We seeded 2 items in inventory_data.py, so should be at least 2
        assert len(data) >= 2


def test_post_inventory_route():
    """POST /inventory should create a new item."""
    payload = {
        "name": "Test Item",
        "price": 1.23,
        "stock": 5,
    }

    with app.test_client() as client:
        response = client.post(
            "/inventory",
            data=json.dumps(payload),
            content_type="application/json",
        )

        assert response.status_code == 201
        data = response.get_json()
        assert isinstance(data, dict)
        assert data["name"] == "Test Item"
        assert data["price"] == 1.23
        assert data["stock"] == 5
        assert "id" in data
