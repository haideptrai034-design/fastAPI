```
# =====================================================
# PHẦN 1: PHÂN TÍCH INPUT / OUTPUT
# =====================================================

# Input của bài toán:
# - Danh sách books.
# - Mỗi sách gồm id, title và quantity.

# Output mong muốn:
# - Trả về JSON gồm:
#   + message
#   + data (danh sách sách sắp hết hàng)

# Điều kiện xác định sách sắp hết hàng:
# - quantity <= 5.
# - Nếu thiếu quantity thì bỏ qua.
# - Nếu quantity âm thì bỏ qua.



# =====================================================
# PHẦN 2: ĐỀ XUẤT ÍT NHẤT 2 GIẢI PHÁP
# =====================================================

# Giải pháp 1:
# Dùng vòng lặp for để duyệt từng quyển sách.
# Kiểm tra quantity.
# Nếu hợp lệ và quantity <= 5 thì thêm vào danh sách kết quả.

# Giải pháp 2:
# Dùng List Comprehension để lọc các sách có quantity <= 5,
# đồng thời kiểm tra quantity tồn tại và không âm.



# =====================================================
# PHẦN 3: SO SÁNH VÀ LỰA CHỌN GIẢI PHÁP
# =====================================================

# Tiêu chí

# Vòng lặp for
# - Độ dễ hiểu: Cao
# - Độ ngắn gọn: Trung bình
# - Dễ xử lý bẫy dữ liệu: Cao
# - Dễ bảo trì: Cao

# List comprehension
# - Độ dễ hiểu: Trung bình
# - Độ ngắn gọn: Cao
# - Dễ xử lý bẫy dữ liệu: Trung bình
# - Dễ bảo trì: Trung bình

# Giải pháp được chọn:
# Vòng lặp for.

# Lý do:
# Dễ đọc, dễ xử lý các trường hợp dữ liệu không hợp lệ
# và dễ mở rộng khi có thêm điều kiện.



# =====================================================
# PHẦN 4: THIẾT KẾ CÁC BƯỚC XỬ LÝ
# =====================================================

# 1. Khởi tạo FastAPI.
# 2. Khai báo danh sách books.
# 3. Tạo endpoint GET /books/low-stock.
# 4. Duyệt danh sách sách.
# 5. Bỏ qua sách thiếu quantity.
# 6. Bỏ qua sách có quantity < 0.
# 7. Lấy các sách có quantity <= 5.
# 8. Nếu không có kết quả thì trả về message phù hợp.
# 9. Nếu có kết quả thì trả về danh sách sách sắp hết hàng.



# =====================================================
# PHẦN 5: TRIỂN KHAI CODE
# =====================================================

from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]

@app.get("/books/low-stock")
def get_low_stock():
    result = []

    for book in books:
        if "quantity" not in book:
            continue

        if book["quantity"] < 0:
            continue

        if book["quantity"] <= 5:
            result.append(book)

    if len(result) == 0:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": result
    }
```
