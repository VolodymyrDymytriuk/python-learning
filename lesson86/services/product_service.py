products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Meat", "price": 250},
    {"id": 3, "name": "Juice", "price": 120},
    {"id": 4, "name": "Bread", "price": 50},
]


def get_all_products(
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    skip: int = 0,
    limit: int = 10
):
    result = products

    if search is not None:
        result = [
            product for product in result
            if search.lower() in product["name"].lower()
        ]

    if min_price is not None:
        result = [
            product for product in result
            if product["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            product for product in result
            if product["price"] <= max_price
        ]

    total = len(result)

    items = result[skip:skip + limit]

    has_next = skip + len(items) < total

    return {
    "total": total,
    "skip": skip,
    "limit": limit,
    "has_next":has_next,
    "items": items
    }



def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return None


def create_product(data: dict):
    new_id = max(
        (product["id"] for product in products),
        default=0
    ) + 1

    new_product = {"id": new_id, **data}
    products.append(new_product)

    return new_product


def update_product(product_id: int, data: dict):
    product = get_product_by_id(product_id)

    if product is None:
        return None

    product.update(data)
    return product


def delete_product(product_id: int):
    product = get_product_by_id(product_id)

    if product is None:
        return False

    products.remove(product)
    return True