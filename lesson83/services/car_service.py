cars = [
    {"id": 1, "brand": "Jeep", "year": 2015, "price": 45000},
    {"id": 2, "brand": "Subaru", "year": 2020, "price": 40000},
    {"id": 3, "brand": "BMW", "year": 2023, "price": 60000},
    {"id": 4, "brand": "Volvo", "year": 2018, "price": 35000},
]



def get_all_cars(
    search: str | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    skip: int = 0,
    limit: int = 10
):
    result = cars

    if search is not None:
        result = [
            car for car in result
            if search.lower() in car["brand"].lower()
        ]

    if min_year is not None:
        result = [
            car for car in result
            if car["year"] >= min_year
        ]

    if max_year is not None:
        result = [
            car for car in result
            if car["year"] <= max_year
        ]

    total = len(result)

    items = result[skip:skip + limit]

    has_next = skip + len(items) < total

    return {
    "total": total,
    "skip": skip,
    "limit": limit,
    "has_next": has_next,
    "items": items
    }


def get_car_by_id(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return car

    return None


def create_car(data: dict):
    new_id = max(
        (car["id"] for car in cars),
        default=0
    ) + 1

    new_car = {"id": new_id, **data}
    cars.append(new_car)

    return new_car


def update_car(car_id: int, data: dict):
    car = get_car_by_id(car_id)

    if car is None:
        return None

    car.update(data)
    return car


def delete_car(car_id: int):
    car = get_car_by_id(car_id)

    if car is None:
        return False

    cars.remove(car)
    return True
