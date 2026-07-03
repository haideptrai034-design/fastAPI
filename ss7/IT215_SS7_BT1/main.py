# STT 1:
# - Dữ liệu gửi lên: order_id = 999
# - Kết quả hiện tại (Mã HTTP + Body): 
#     + Mã HTTP: 200 OK
#     + Body: {"message": "Order not found"}
# - Kết quả đúng mong muốn: 
#     + Mã HTTP: 404 Not Found
#     + Body: {"detail": "Order not found"}
# - Lỗi phát hiện: 
#     Lỗi mã trạng thái "ảo" (False Status Code) - Không tìm thấy tài nguyên nhưng hệ thống 
#     vẫn trả về mã trạng thái thành công 200 OK thay vì chuẩn RESTful 404 Not Found.

# STT 2:
# - Dữ liệu gửi lên: order_id = 1
# - Kết quả hiện tại (Mã HTTP + Body): 
#     + Mã HTTP: 200 OK
#     + Body: {
#         "id": 1, 
#         "customer_name": "Nguyen Van A", 
#         "total_amount": 1500000.0, 
#         "profit_margin": 0.25, 
#         "supplier_id": "SUP_DELL_01"
#       }
# - Kết quả đúng mong muốn: 
#     + Mã HTTP: 200 OK
#     + Body: {
#         "id": 1, 
#         "customer_name": "Nguyen Van A", 
#         "total_amount": 1500000.0
#       }
# - Lỗi phát hiện: 
#     Lỗi lộ thông tin nhạy cảm (Data Leakage) - API trả về toàn bộ dữ liệu nội bộ bao gồm 
#     cả biên lợi nhuận (`profit_margin`) và ID nhà cung ứng (`supplier_id`), vi phạm nghiêm 
#     trọng quy chuẩn an toàn thông tin.

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# 1. Giữ nguyên Dữ liệu nội bộ trong bộ nhớ tạm
orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,
        "supplier_id": "SUP_DELL_01"
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,       
        "supplier_id": "SUP_LOGI_02"  
    }
]

# 2. Khai báo Schema nhận dữ liệu đầy đủ từ DB
class OrderInternal(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    profit_margin: float
    supplier_id: str

# 3. Tạo Schema phản hồi công khai
class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_amount: float

# 4. API Endpoint đã sửa lỗi
@app.get(
    "/orders/{order_id}", 
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK
)
def get_order_detail(order_id: int):
    for order in orders_db:
        if order["id"] == order_id:
            return order
            
    # Trả về lỗi chuẩn RESTful 404 thay vì trả về message kèm 200 OK
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Order not found"
    )