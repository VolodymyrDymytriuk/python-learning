
from collections.abc import Iterator


def get_request_context() -> Iterator[dict[str, str]]:
    print("1. OPEN resource")

    context = {
        "status": "connected",
        "resource": "test-database"
    }

    try:
        yield context
    finally:
        print("3. CLOSE resource")
