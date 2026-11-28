
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

def test_create_car(client: TestClient):
    new_car = {
        "brand": "Toyota",
        "year": 2021,
        "price": 30000
    }

    response = client.post("/cars", json=new_car)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 5
    assert data["brand"] == "Toyota"
    assert data["year"] == 2021
    assert data["price"] == 30000

    # Перевіряємо, що авто доступне через GET
    get_response = client.get("/cars/5")

    assert get_response.status_code == 200
    assert get_response.json()["brand"] == "Toyota"

def test_create_car_invalid_year(client: TestClient):
    response = client.post(
        "/cars",
        json={
            "brand": "Toyota",
            "year": "invalid-year",
            "price": 30000
        }
    )

    assert response.status_code == 422

def test_put_car(client: TestClient):
    updated_car = {
        "brand": "Audi",
        "year": 2024,
        "price": 55000
    }

    response = client.put(
        "/cars/1",
        json=updated_car
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["brand"] == "Audi"
    assert data["year"] == 2024
    assert data["price"] == 55000

    get_response = client.get("/cars/1")

    assert get_response.json()["brand"] == "Audi"

def test_put_car_not_found(client: TestClient):
    response = client.put(
        "/cars/999",
        json={
            "brand": "Audi",
            "year": 2024,
            "price": 55000
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

def test_patch_car(client: TestClient):
    response = client.patch(
        "/cars/1",
        json={"price": 39000}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["price"] == 39000

    # Поля, які не передавали, не повинні змінитися
    assert data["brand"] == "Jeep"
    assert data["year"] == 2015

def test_patch_car_null(client: TestClient):
    response = client.patch(
        "/cars/1",
        json={"brand": None}
    )

    assert response.status_code == 422

    get_response = client.get("/cars/1")

    assert get_response.json()["brand"] == "Jeep"

def test_delete_car(client: TestClient):
    response = client.delete("/cars/1")

    assert response.status_code == 204
    assert response.content == b""

    # Видалений автомобіль більше не існує
    get_response = client.get("/cars/1")

    assert get_response.status_code == 404

    # Кількість автомобілів зменшилася
    list_response = client.get("/cars")

    assert list_response.json()["total"] == 3

def test_delete_car_not_found(client: TestClient):
    response = client.delete("/cars/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

def test_create_product(client: TestClient):
    response = client.post(
        "/products",
        json={
            "name": "Cheese",
            "price": 180
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 5
    assert data["name"] == "Cheese"
    assert data["price"] == 180

    get_response = client.get("/products/5")

    assert get_response.status_code == 200


def test_put_product(client: TestClient):
    response = client.put(
        "/products/1",
        json={
            "name": "Organic Milk",
            "price": 110
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Organic Milk"
    assert response.json()["price"] == 110


def test_patch_product(client: TestClient):
    response = client.patch(
        "/products/1",
        json={"price": 105}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Milk"
    assert response.json()["price"] == 105


def test_delete_product(client: TestClient):
    response = client.delete("/products/1")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get("/products/1")

    assert get_response.status_code == 404
    
def test_initial_data_unchanged(client: TestClient):
    cars_response = client.get("/cars")
    products_response = client.get("/products")

    assert cars_response.status_code == 200
    assert products_response.status_code == 200

    assert cars_response.json()["total"] == 4
    assert products_response.json()["total"] == 4

    car = client.get("/cars/1").json()
    product = client.get("/products/1").json()

    assert car["brand"] == "Jeep"
    assert car["price"] == 45000

    assert product["name"] == "Milk"
    assert product["price"] == 90

def test_patch_car_not_found(client: TestClient):
    response = client.patch(
        "/cars/999",
        json={"price": 39000}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Car not found"

def test_create_product_invalid_price(client: TestClient):
    response = client.post(
        "/products",
        json={
            "price": "Invalid-price"
        }
    )

    assert response.status_code == 422

def test_patch_car_missing_body(client: TestClient):
    response = client.patch("/cars/999")

    assert response.status_code == 422

def test_delete_product_not_found(client: TestClient):
    response = client.delete("/products/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
