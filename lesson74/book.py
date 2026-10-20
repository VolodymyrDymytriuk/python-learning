from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
    {"id": 3, "title": "Django", "price": 600},
    {"id": 4, "title": "SQL", "price": 300},
]

class BookResponse(BaseModel):
    id: int
    title: str
    price: float


class BookListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[BookResponse]

class BookCreate(BaseModel):
    title: str
    price: float

class BookUpdate(BaseModel):
    title: str | None = None
    price: float | None = None

@app.post(
    "/books",
    response_model=BookResponse, status_code=201
)
def create_book(book: BookCreate):
    
    new_id = max((book["id"] 
                  for book in books ),
                    default = 0
                ) + 1
    
    new_book = {
        "id": new_id,
        "title": book.title,
        "price": book.price
    }

    books.append(new_book)

    return new_book   

@app.get("/books", response_model=BookListResponse)
def get_books(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=50
    ),
    min_price: float | None = Query(
            default=None,
            gt=0
    ),
    max_price: float | None = Query(
            default=None,
            gt=0
    ),
    skip: int = Query(
        default=0,
        ge=0
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    )
):
    
    result = books

    if search is not None:
        result = [
            book
            for book in result
            if search.lower() in book["title"].lower()
        ]
        
    if min_price is not None:
        result = [
            book
            for book in result
            if book["price"] >= min_price
        ]
    
    if max_price is not None:
        result = [
            book
            for book in result
            if book["price"] <= max_price
        ]

    total = len(result)
        
    items = result[skip:skip + limit]
        
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }
@app.get(
    "/books/{book_id}",
    response_model=BookResponse, responses={404:{"description":"Book not found"}}
)
def get_book(book_id: int):

    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )
@app.delete("/books/{book_id}", status_code=204, responses={404: {"description": "Book not found"}})
def delete_book(book_id: int):

    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

@app.put(
    "/books/{book_id}",
    response_model=BookResponse,
    responses={404: {"description": "Book not found"}}
)
def update_book(book_id: int, book_data: BookCreate):

    for book in books:
        if book["id"] == book_id:
            book["title"] = book_data.title
            book["price"] = book_data.price

            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

@app.patch(
    "/books/{book_id}",
    response_model=BookResponse,
    responses={404: {"description": "Book not found"}}
)
def patch_book(book_id: int, book_update: BookUpdate):

    for book in books:
        if book["id"] == book_id:

            update_data = book_update.model_dump(
                exclude_unset=True
            )

            if any(value is None for value in update_data.values()):
                raise HTTPException(
                    status_code=422,
                    detail="Fields cannot be null"
                )

            book.update(update_data)

            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )