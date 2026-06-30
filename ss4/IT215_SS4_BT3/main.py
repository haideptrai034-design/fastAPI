# 1. Input của bài toán
# API nhận request dạng:
# GET /products
# GET /products?keyword=mouse
# GET /products?max_price=1000000
# GET /products?keyword=mouse&max_price=300000

# Gồm 2 Query Parameters:
# - keyword (string, không bắt buộc): tìm theo tên sản phẩm
# - max_price (float, không bắt buộc): lọc theo giá tối đa

# 2. Output mong muốn
# - Trả về danh sách sản phẩm (JSON)
# - Hoặc trả lỗi nếu dữ liệu không hợp lệ

# Ví dụ:
# [
#   {"id": 2, "name": "Mouse", "price": 200000}
# ]

# 3. Giải pháp xử lý
# - Lấy danh sách sản phẩm
# - Kiểm tra max_price có hợp lệ không
# - Lọc theo keyword (không phân biệt hoa thường)
# - Lọc theo max_price
# - Trả kết quả

# 4. Các bước xử lý

# Trường hợp 1: Không có query → trả toàn bộ

# Trường hợp 2: Có keyword → lọc theo tên
# keyword.lower() in product["name"].lower()

# Trường hợp 3: Có max_price → lọc theo giá
# product["price"] <= max_price

# Trường hợp 4: Có cả 2 → thỏa cả 2 điều kiện

# 5. Bẫy dữ liệu
# Nếu max_price < 0 → trả lỗi:

# {
#   "detail": "max_price không được âm"
# }

from fastapi import FastAPI, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):

    # Validate max_price
    if max_price is not None and max_price < 0:
        raise HTTPException(
            status_code=400,
            detail="max_price không được âm"
        )

    result = products

    # Lọc theo keyword
    if keyword:
        result = [
            product for product in result
            if keyword.lower() in product["name"].lower()
        ]

    # Lọc theo giá
    if max_price is not None:
        result = [
            product for product in result
            if product["price"] <= max_price
        ]

    return result