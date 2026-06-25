"""Example test style for the test-writer skill."""
import pytest


class TestCreateItem:
    """Tests for item creation."""

    def test_create_item_valid(self, client):
        """Happy path: create an item with valid data."""
        response = client.post("/items", json={
            "name": "Widget",
            "price": 9.99,
            "quantity": 5,
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Widget"
        assert data["price"] == 9.99

    def test_create_item_missing_name(self, client):
        """Error case: missing required field."""
        response = client.post("/items", json={"price": 9.99})
        assert response.status_code == 422

    def test_create_item_negative_price(self, client):
        """Edge case: negative price should be rejected."""
        response = client.post("/items", json={
            "name": "Widget",
            "price": -1.0,
        })
        assert response.status_code == 422
