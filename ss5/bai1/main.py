"""
Phần 1: Chỉ ra lỗi bằng test case
STT	Dữ liệu gửi lên	Kết quả hiện tại	Kết quả đúng mong muốn	Lỗi phát hiện
1	code = "SP001", name = "Laptop Asus", price = 18000000, stock = 5	API vẫn tạo sản phẩm mới	API phải báo lỗi vì mã SP001 đã tồn tại	Không kiểm tra trùng mã sản phẩm
2	code = "SP002", name = "Mouse Gaming", price = 500000, stock = 20	API vẫn tạo sản phẩm mới	API phải báo lỗi vì mã SP002 đã tồn tại	Cho phép tạo nhiều sản phẩm có cùng mã
Ví dụ Request Test Case 1
POST /products

{
    "code": "SP001",
    "name": "Laptop Asus",
    "price": 18000000,
    "stock": 5
}
Kết quả hiện tại
{
    "message": "Create product successfully",
    "data": {
        "id": 3,
        "code": "SP001",
        "name": "Laptop Asus",
        "price": 18000000,
        "stock": 5
    }
}

➡ Sai vì SP001 đã tồn tại.

Ví dụ Request Test Case 2
POST /products

{
    "code": "SP002",
    "name": "Mouse Gaming",
    "price": 500000,
    "stock": 20
}
Kết quả hiện tại
{
    "message": "Create product successfully",
    "data": {
        "id": 3,
        "code": "SP002",
        "name": "Mouse Gaming",
        "price": 500000,
        "stock": 20
    }
}

➡ Sai vì SP002 đã tồn tại.

Phần 2: Sửa source code
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]


class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):

    # Kiểm tra mã sản phẩm đã tồn tại hay chưa
    for p in products:
        if p["code"] == product.code:
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    # Tạo sản phẩm mới
    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }