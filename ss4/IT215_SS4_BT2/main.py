# Phần 1: Phân tích lỗi
# Endpoint hiện tại có Path Parameter
# @app.get("/orders/status/{status}")
# Path Parameter trong bài là biến status
# Khi gọi /orders/status/pending thì status nhận = "pending"
# Vì sao API trả về sai dữ liệu?
# Vì không sử dụng biến status trong logic
# Dòng code gây lỗi
# return orders -> trả về toàn bộ ds -> bỏ qua filter

from fastapi import FastAPI
app = FastAPI()
orders = [
{"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
{"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
{"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
{"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]
@app.get("/orders/status/{status}")
def get_order_by_status(status:str):
    # Ds status hợp lệ
    valid_status=["pending","paid","cencelled"]
    # Kiểm tra hợp lệ
    if status not in valid_status:
        return {
            "massage":"Trạng thái đơn hàng không hợp lệ"
        }
    # Lọc dữ liệu
    result=[]
    for order in orders:
        if order["status"]==status:
            result.append(order)
    return result
