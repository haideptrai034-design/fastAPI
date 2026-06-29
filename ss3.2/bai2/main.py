from fastapi import FastAPI

app = FastAPI()

# Danh sách sách
books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Lê Minh Thu",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Phạm Lan Hồng",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Lê Minh Huyền",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Lê Ánh Linh",
        "category": "programming",
        "year": 2008,
        "is_available": False
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vũ Hồng Vân",
        "category": "network",
        "year": 2019,
        "is_available": True
    }
]


# API kiểm tra hệ thống
@app.get("/health")
def health():
    return {
        "message": "Library API is running"
    }


# API lấy toàn bộ danh sách sách
@app.get("/books")
def get_books():
    return books


# API lấy danh sách sách còn có thể mượn
@app.get("/books/available")
def get_available_books():
    result = []

    for book in books:
        if book["is_available"] == True:
            result.append(book)

    return result


# API lấy danh sách sách đang được mượn
@app.get("/books/borrowed")
def get_borrowed_books():
    result = []

    for book in books:
        if book["is_available"] == False:
            result.append(book)

    return result