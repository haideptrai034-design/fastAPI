# 1. PHÂN TÍCH BÀI TOÁN (INPUT / OUTPUT):
#    - Input Request (Dữ liệu gửi lên):
#      + product_id (int): ID của sản phẩm muốn mua.
#      + quantity (int): Số lượng sản phẩm đặt mua.
#    - Output Response (Kết quả trả về):
#      + Khi thành công: HTTP 201 Created kèm thông tin đơn hàng mới tạo và thông báo thành công.
#      + Khi thất bại: HTTP 400 Bad Request kèm thông báo lỗi cụ thể (Sản phẩm không đủ hàng, số lượng âm, v.v.).

# 2. THIẾT KẾ CÁC BƯỚC XỬ LÝ (LOGIC FLOW):
#    - Bước 1: Tiếp nhận Request thông qua Pydantic Model. Chặn ngay tại tầng validation nếu quantity <= 0.
#    - Bước 2: Tìm kiếm sản phẩm trong `products_db` bằng `product_id`.
#              -> Nếu không thấy: Raise HTTPException 404 Not Found (Sản phẩm không tồn tại).
#    - Bước 3: Kiểm tra số lượng tồn kho (`stock`) của sản phẩm đó.
#              -> Nếu `quantity` > `stock`: Raise HTTPException 400 Bad Request ("Sản phẩm không đủ số lượng trong kho").
#    - Bước 4: Nếu mọi điều kiện hợp lệ:
#              -> Tiến hành trừ bớt số lượng kho: `product["stock"] -= quantity`
#              -> Tạo ID ngẫu nhiên hoặc tự tăng cho đơn hàng mới.
#              -> Tính toán `total_amount = quantity * product["price"]`
#              -> Thêm đơn hàng vào `orders_db`.
#    - Bước 5: Trả về HTTP Status Code 201 Created cùng dữ liệu đơn hàng.


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
from typing import List

app = FastAPI()

# Dữ liệu giả lập ban đầu theo yêu cầu đề bài
products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []

# 1. Định nghĩa Input Schema (Dữ liệu đầu vào)
class OrderCreate(BaseModel):
    product_id: int
    quantity: int

    # Bẫy 2: Chặn số lượng đặt không hợp lệ (<= 0) ngay tại tầng Pydantic Validation
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Số lượng mua phải lớn hơn 0")
        return value

# 2. Định nghĩa Output Schema (Dữ liệu trả về khi tạo thành công)
class OrderResponse(BaseModel):
    order_id: int
    product_id: int
    product_name: str
    quantity: int
    total_amount: float

# Helper endpoint để kiểm tra danh sách kho hàng và đơn hàng hiện tại
@app.get("/data-debug")
def get_current_data():
    return {"products": products_db, "orders": orders_db}

# 3. API Endpoint Khởi tạo đơn hàng
@app.post(
    "/orders", 
    response_model=OrderResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_order(order_data: OrderCreate):
    # Bước 1: Tìm kiếm sản phẩm trong database dựa vào product_id gửi lên
    product = next((p for p in products_db if p["id"] == order_data.product_id), None)
    
    # Kiểm tra quy tắc 1: Nếu sản phẩm không tồn tại
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sản phẩm không tồn tại trên hệ thống"
        )
        
    # Bẫy 1: Kiểm tra số lượng đặt vượt quá tồn kho
    if order_data.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )
        
    # Bước 2: Trừ bớt số lượng hàng trong kho
    product["stock"] -= order_data.quantity
    
    # Bước 3: Tính toán tổng tiền và tạo bản ghi đơn hàng mới
    new_order_id = len(orders_db) + 1
    total_price = order_data.quantity * product["price"]
    
    new_order = {
        "order_id": new_order_id,
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": order_data.quantity,
        "total_amount": total_price
    }
    
    # Lưu vào database giả lập
    orders_db.append(new_order)
    
    # Bước 4: Trả về kết quả kèm mã trạng thái 201 Created
    return new_order