from copy import deepcopy

import pytest

from services import car_service, product_service


# Зберігаємо початкові дані
INITIAL_CARS = deepcopy(car_service.cars)
INITIAL_PRODUCTS = deepcopy(product_service.products)


@pytest.fixture(autouse=True)
def isolated_data(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(
        car_service,
        "cars",
        deepcopy(INITIAL_CARS)
    )

    monkeypatch.setattr(
        product_service,
        "products",
        deepcopy(INITIAL_PRODUCTS)
    )