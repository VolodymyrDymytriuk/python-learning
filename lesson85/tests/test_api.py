
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from main import app
from dependencies.request_context import get_request_context


@pytest.fixture
def context_events() -> list[str]:
    return []


@pytest.fixture
def client(
    context_events: list[str]
) -> Iterator[TestClient]:

    def fake_request_context() -> Iterator[dict[str, str]]:
        context_events.append("OPEN")

        try:
            yield {
                "status": "connected",
                "resource": "mock-database"
            }
        finally:
            context_events.append("CLOSE")

    app.dependency_overrides[
        get_request_context
    ] = fake_request_context

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_get_cars(client: TestClient):
    response = client.get("/cars")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 4
    assert len(data["items"]) == 4
    assert data["has_next"] is False


def test_cars_pagination(client: TestClient):
    response = client.get("/cars?skip=1&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 4
    assert data["skip"] == 1
    assert data["limit"] == 2
    assert data["has_next"] is True
    assert len(data["items"]) == 2

    assert [car["id"] for car in data["items"]] == [2, 3]


def test_cars_filter(client: TestClient):
    response = client.get("/cars?min_year=2020")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2

    assert [car["id"] for car in data["items"]] == [2, 3]


def test_car_not_found(client: TestClient):
    response = client.get("/cars/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"


def test_invalid_skip(client: TestClient):
    response = client.get("/cars?skip=-1")

    assert response.status_code == 422


def test_invalid_limit(client: TestClient):
    response = client.get("/cars?limit=0")

    assert response.status_code == 422


def test_products_filter(client: TestClient):
    response = client.get("/products?min_price=100")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert [product["id"] for product in data["items"]] == [2, 3]


def test_dependency_override(
    client: TestClient,
    context_events: list[str]
):
    response = client.get("/cars/1")

    assert response.status_code == 200
    assert response.json()["brand"] == "Jeep"

    assert context_events == ["OPEN", "CLOSE"]

def test_get_product_by_id(
    client: TestClient,
    context_events: list[str]
):
    response = client.get("/products/1")
    
    assert response.status_code == 200
    assert response.json()["name"] == "Milk"
    assert response.json()["price"] == 90
    
    assert context_events == ["OPEN", "CLOSE"]
            
def test_product_not_found(client: TestClient):
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_skip_too_large(client: TestClient):
    response = client.get("/products?skip=1001")

    assert response.status_code == 422
    assert response.json()["detail"] == "skip cannot be greater than 1000"