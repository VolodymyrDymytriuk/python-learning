products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Meat", "price": 250},
    {"id": 3, "name": "Juice", "price": 120},
    {"id": 4, "name": "Bread", "price": 50},
]

def get_all_products():
    return products


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