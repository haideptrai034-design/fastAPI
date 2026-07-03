# 1. PHÂN TÍCH INPUT / OUTPUT:
#    - Input Request (Dữ liệu nhận vào):
#      + order_id (int) thông qua Path Parameter: ID của đơn hàng cần tra cứu lịch sử thanh toán.
#    - Output Response (Kết quả trả về):
#      + Khi thành công (200 OK): Trả về cấu trúc gồm trạng thái thanh toán và phương thức thanh toán.
#        Ví dụ: {"payment_status": "PAID", "method": "BANK_TRANSFER"}
#      + Khi không tìm thấy đơn hàng (404 Not Found): {"detail": "Không tìm thấy thông tin thanh toán cho đơn hàng này"}
#      + Khi hệ thống gặp sự cố bất ngờ (500 Internal Server Error): Trả về thông báo lỗi thân thiện, bảo mật, 
#        chặn đứng hoàn toàn việc lộ Stack Trace: {"detail": "Hệ thống đang bận, vui lòng thử lại sau"}

# 2. ĐỀ XUẤT GIẢI PHÁP LƯU TRỮ VÀ TRA CỨU:
#    - Giải pháp 1 (Duyệt Tuyến Tính - List): 
#      Dữ liệu lưu dạng mảng `[{"id": 1, ...}, {"id": 2, ...}]`. Khi có request, hệ thống chạy vòng lặp 
#      từ đầu đến cuối mảng để so khớp `id == order_id`.
#    - Giải pháp 2 (Bảng Tra Cứu Nhanh - Dict): 
#      Chuyển đổi cấu trúc dữ liệu thô sang dạng Dictionary với Key chính là `id` của đơn hàng.
#      Ví dụ: `{1: {"code": "SP001", ...}, 2: {"code": "SP002", ...}}`. Khi tra cứu chỉ cần gọi trực tiếp qua Key.

# Bảng so sánh

# | Tiêu chí          | Giải pháp 1: Duyệt List (Mảng)        | Giải pháp 2: Dùng Dict (Từ điển)       |
# |:------------------|:--------------------------------------|:---------------------------------------|
# | Tốc độ tìm kiếm   | Chậm. Độ phức tạp O(n). Dữ liệu lớn  | Cực nhanh. Độ phức tạp O(1) nhờ cơ chế |
# |                   | sẽ gây ra High Latency (Trễ cao).     | băm (Hash map), không phụ thuộc số lượng|
# | Bộ nhớ tiêu hao   | Ít tốn bộ nhớ hơn vì lưu tuyến tính.  | Tốn bộ nhớ hơn một chút để lưu cấu trúc|
# |                   |                                        | các Key và bảng băm thông tin.         |
# | Độ dễ hiểu        | Rất trực quan, lập trình viên cơ bản  | Đòi hỏi tư duy cấu trúc hóa dữ liệu    |
# |                   | đều quen thuộc với vòng lặp for/next. | tốt hơn, cấu trúc phức tạp hơn tí.     |
# | Khả năng bảo trì  | Khó mở rộng khi dữ liệu tăng lên      | Dễ quản lý, bảo trì tốt cho hệ thống   |
# |                   | hàng vạn đơn hàng mỗi ngày.           | chịu tải cao và dữ liệu lớn.           |
# | Bối cảnh phù hợp  | Mảng nhỏ, dữ liệu ít biến động.       | Hệ thống có tần suất đọc/tra cứu lớn   |
# |                   |                                        | và dữ liệu phát sinh liên tục.         |

# * KẾT LUẬN LỰA CHỌN:
#   Hệ thống được mô tả phát sinh hàng vạn đơn hàng mỗi ngày. Do đó, tốc độ xử lý và độ trễ (Latency) 
#   là ưu tiên hàng đầu. Ta quyết định LỰA CHỌN GIẢI PHÁP 2 (DÙNG DICT). Việc đánh đổi một chút bộ nhớ 
#   để lấy tốc độ tìm kiếm tối ưu O(1) là hoàn toàn xứng đáng cho bài toán này.

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

orders_list = [
    {"id": 1, "code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    {"id": 2, "code": "SP002", "payment_status": "UNPAID", "method": "NONE"}
]

orders_dict = {order["id"]: order for order in orders_list}

class PaymentResponse(BaseModel):
    payment_status: str
    method: str


@app.get(
    "/orders/{order_id}/payment", 
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK
)
def get_order_payment_history(order_id: int):
    try:
        order_payment = orders_dict.get(order_id)
        if not order_payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông tin thanh toán cho đơn hàng này"
            )
            
        return order_payment

    except HTTPException as http_ex:
        raise http_ex
        
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Hệ thống đang bận, vui lòng thử lại sau"
        )