"""
PHẦN 1: PHÂN TÍCH & ĐỀ XUẤT ĐA GIẢI PHÁP
1. Phân tích Input/Output
Input

API sử dụng phương thức PUT /products/{product_id}

Path Parameter
product_id: ID của sản phẩm cần cập nhật.
Request Body
{
    "code": "SP003",
    "name": "Gaming Keyboard",
    "price": 600000,
    "stock": 8
}

Gồm các trường:

code: Mã sản phẩm.
name: Tên sản phẩm.
price: Giá bán.
stock: Số lượng tồn kho.
Output khi thành công
HTTP Status: 200 OK
{
    "message": "Update product successfully",
    "data": {
        "id": 1,
        "code": "SP003",
        "name": "Gaming Keyboard",
        "price": 600000,
        "stock": 8
    }
}
Output khi thất bại
Sản phẩm không tồn tại
{
    "detail": "Product not found"
}

HTTP Status:

404 Not Found
Mã sản phẩm bị trùng
{
    "detail": "Product code already exists"
}

HTTP Status:

400 Bad Request
Tên sản phẩm rỗng
{
    "detail": "Product name cannot be empty"
}

HTTP Status:

400 Bad Request
Giá không hợp lệ
{
    "detail": "Price must be greater than 0"
}

HTTP Status:

400 Bad Request
Tồn kho không hợp lệ
{
    "detail": "Stock must be greater than or equal to 0"
}

HTTP Status:

400 Bad Request
2. Đề xuất tối thiểu 2 giải pháp
Giải pháp 1: Duyệt List
Cách xử lý
Duyệt danh sách products để tìm product_id.
Nếu không tìm thấy → báo lỗi 404.
Duyệt tiếp danh sách để kiểm tra code có bị trùng với sản phẩm khác không.
Kiểm tra name, price, stock.
Cập nhật dữ liệu.
Trả về sản phẩm sau khi cập nhật.
Ưu điểm
Dễ hiểu.
Dễ viết.
Phù hợp khi dữ liệu ít.
Nhược điểm
Mỗi lần tìm phải duyệt toàn bộ danh sách.
Hiệu năng giảm khi dữ liệu lớn.
Giải pháp 2: Dùng Dictionary

Ví dụ:
"""
products = {
    1: {
        "id": 1,
        "code": "SP001",
        "name": "Keyboard",
        "price": 500000,
        "stock": 10
    },
    2: {
        "id": 2,
        "code": "SP002",
        "name": "Mouse",
        "price": 300000,
        "stock": 5
    }
}
"""
Cách xử lý
Kiểm tra product_id bằng khóa của dictionary.
Nếu không tồn tại → báo lỗi.
Duyệt các giá trị để kiểm tra mã sản phẩm trùng.
Kiểm tra dữ liệu hợp lệ.
Cập nhật trực tiếp.
Ưu điểm
Tìm kiếm theo ID rất nhanh.
Dễ mở rộng.
Phù hợp dữ liệu lớn.
Nhược điểm
Tốn bộ nhớ hơn.
Cấu trúc phức tạp hơn.
PHẦN 2: SO SÁNH & LỰA CHỌN GIẢI PHÁP
Tiêu chí	Giải pháp 1: Duyệt List	Giải pháp 2: Dùng Dict
Tốc độ tìm kiếm	Chậm (O(n))	Nhanh (O(1))
Bộ nhớ	Ít	Nhiều hơn
Dễ hiểu	Rất dễ	Khó hơn một chút
Dễ bảo trì	Tốt với dự án nhỏ	Tốt với dự án lớn
Bối cảnh phù hợp	Dữ liệu ít, bài tập	Hệ thống thực tế, dữ liệu lớn
Kết luận lựa chọn

Đối với bài tập FastAPI hiện tại, giải pháp dùng List là phù hợp vì đơn giản, dễ hiểu và đúng với cấu trúc dữ liệu đã cho. Trong các hệ thống thực tế có nhiều dữ liệu, Dictionary sẽ là lựa chọn tốt hơn nhờ tốc độ truy cập nhanh.

PHẦN 3: TRIỂN KHAI CODE
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]


class ProductUpdate(BaseModel):
    code: str
    name: str
    price: float
    stock: int


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):

    # Tìm sản phẩm theo ID
    current_product = None
    for p in products:
        if p["id"] == product_id:
            current_product = p
            break

    if current_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Kiểm tra mã sản phẩm trùng
    for p in products:
        if (
            p["code"] == product.code
            and p["id"] != product_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    # Kiểm tra tên sản phẩm
    if product.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Product name cannot be empty"
        )

    # Kiểm tra giá
    if product.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be greater than 0"
        )

    # Kiểm tra tồn kho
    if product.stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Stock must be greater than or equal to 0"
        )

    # Cập nhật thông tin
    current_product["code"] = product.code
    current_product["name"] = product.name
    current_product["price"] = product.price
    current_product["stock"] = product.stock

    return {
        "message": "Update product successfully",
        "data": current_product
    }