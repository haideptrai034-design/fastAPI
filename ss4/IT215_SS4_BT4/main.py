# 1. Input của bài toán

# API nhận request:
# POST /students

# Dữ liệu gửi lên dạng JSON:
# {
#   "full_name": "Nguyen Van A",
#   "email": "vana@gmail.com",
#   "age": 20,
#   "course": "python",
#   "phone": "0987654321"
# }

# 2. Output mong muốn

# Trường hợp thành công:
# {
#   "message": "Thêm học viên thành công",
#   "data": {...}
# }

# Trường hợp thất bại:
# - Thiếu field → lỗi validate
# - Email sai định dạng → lỗi validate
# - Email trùng → 
# {
#   "detail": "Email đã tồn tại trong hệ thống"
# }

# 3. Giải pháp 1: Validate thủ công

# - Dùng if/else để kiểm tra từng field
# - Kiểm tra:
#   + full_name
#   + email format
#   + email trùng

# Ưu điểm:
# - Dễ hiểu

# Nhược điểm:
# - Code dài
# - Khó mở rộng
# - Khó bảo trì

# 4. Giải pháp 2: Dùng Pydantic (Khuyên dùng)

# - Tạo class Student
# - Dùng kiểu dữ liệu để validate
# - Dùng EmailStr kiểm tra email

# Ưu điểm:
# - Code gọn
# - Validate tự động
# - Rõ ràng

# Nhược điểm:
# - Cần hiểu Pydantic

# Tiêu chí                 Giải pháp 1        Giải pháp 2
# ------------------------------------------------------
# Độ dễ hiểu              Dễ                 Trung bình
# Số lượng code           Nhiều              Ít
# Kiểm soát lỗi           Kém                Tốt
# Cấu trúc dữ liệu        Không rõ           Rõ ràng

# Lựa chọn: Giải pháp 2 (Pydantic)

# Lý do:
# - Code ngắn gọn
# - Validate mạnh
# - Phù hợp FastAPI
# - Dễ mở rộng

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI()

# Fake database
students_db = []

# Model
class Student(BaseModel):
    full_name: str
    email: EmailStr
    age: int
    course: str
    phone: str

    # Validate full_name
    @field_validator("full_name")
    def validate_name(cls, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("full_name phải có ít nhất 3 ký tự")
        return value

@app.post("/students")
def create_student(student: Student):

    # Kiểm tra email trùng
    for s in students_db:
        if s["email"] == student.email:
            raise HTTPException(
                status_code=400,
                detail="Email đã tồn tại trong hệ thống"
            )

    # Lưu vào database
    students_db.append(student.model_dump())

    return {
        "message": "Thêm học viên thành công",
        "data": student
    }