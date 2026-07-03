# STT 1:
# - Dữ liệu/Endpoint gửi lên: PUT /orders/999/status với status="SHIPPING"
# - Kết quả hiện tại (Mã HTTP + Body): 
#     + Mã HTTP: 200 OK
#     + Body: {"statusCode": 200, "message": "Cập nhật thành công", "data": null}
# - Kết quả đúng mong muốn: 
#     + Mã HTTP: 404 Not Found
#     + Body: {"detail": "Order not found"}
# - Lỗi phát hiện: 
#     Lọt luồng xử lý lỗi (Luồng code bên dưới vẫn chạy dù không tìm thấy đơn hàng). 
#     Hệ thống chỉ dùng lệnh `print()` để log chứ không chặn lại, dẫn đến việc trả về mã 
#     thành công 200 OK "ảo" với dữ liệu `data` bị null.

# STT 2:
# - Dữ liệu/Endpoint gửi lên: PUT /orders/1/status với status="TRONG_SANG"
# - Kết quả hiện tại (Mã HTTP + Body): 
#     + Mã HTTP: 200 OK
#     + Body: {"error": "Trạng thái không hợp lệ"}
# - Kết quả đúng mong muốn: 
#     + Mã HTTP: 400 Bad Request
#     + Body: {"detail": "Trạng thái không hợp lệ. Chỉ chấp nhận: PENDING, SHIPPING, DELIVERED"}
# - Lỗi phát hiện: 
#     Sử dụng "Magic Number" (Tự định nghĩa trạng thái lỗi trong chuỗi trả về thay vì dùng 
#     mã HTTP Standard). Đồng thời lọt luồng xử lý lỗi khi dùng `return` dạng dictionary 
#     ở giữa hàm, không tận dụng cơ chế `raise HTTPException` để chặn dữ liệu sai từ đầu.


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator

app = FastAPI()

# Giữ nguyên dữ liệu giả lập trong bộ nhớ tạm
orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

# Định nghĩa danh sách các trạng thái hợp lệ
VALID_STATUSES = ["PENDING", "SHIPPING", "DELIVERED"]

class StatusUpdate(BaseModel):
    status: str

    # Sử dụng Pydantic Validator để chặn dữ liệu sai ngay từ vòng gửi xe
    @field_validator('status')
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in VALID_STATUSES:
            raise ValueError(f"Trạng thái không hợp lệ. Chỉ chấp nhận: {', '.join(VALID_STATUSES)}")
        return value

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    return order

@app.put("/orders/{order_id}/status", status_code=status.HTTP_200_OK)
def update_order_status(order_id: int, data: StatusUpdate):
    # Tìm kiếm đơn hàng trong danh sách
    order = next((o for o in orders_db if o["id"] == order_id), None)
    
    # "Sai thì raise" - Chặn lỗi không tồn tại đơn hàng ngay lập tức
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found!"
        )
        
    # Cập nhật trạng thái mới
    order["status"] = data.status

    # Trả về kết quả đúng chuẩn RESTful
    return {
        "message": "Cập nhật thành công", 
        "data": order
    }