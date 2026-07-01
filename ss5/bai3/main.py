"""
PHẦN 1: PHÂN TÍCH VÀ THIẾT KẾ GIẢI PHÁP
1. Phân tích bài toán
Input API

API sử dụng phương thức POST /registrations.

Dữ liệu nhận từ người dùng:

{
    "student_id": 1,
    "course_id": 2
}

Gồm hai trường:

student_id: ID của học viên.
course_id: ID của khóa học.
Output khi thành công
HTTP Status: 201 Created
{
    "message": "Registration created successfully",
    "data": {
        "id": 3,
        "student_id": 1,
        "course_id": 2
    }
}
Output khi thất bại
Học viên không tồn tại
{
    "detail": "Student not found"
}

HTTP Status:

404 Not Found
Khóa học không tồn tại
{
    "detail": "Course not found"
}

HTTP Status:

404 Not Found
Đăng ký trùng
{
    "detail": "Student already registered this course"
}

HTTP Status:

400 Bad Request
Khóa học đã đủ sĩ số
{
    "detail": "Course is full"
}

HTTP Status:

400 Bad Request
2. Đề xuất giải pháp

Các bước xử lý:

Nhận dữ liệu từ request.
Kiểm tra student_id có tồn tại trong danh sách students.
Kiểm tra course_id có tồn tại trong danh sách courses.
Kiểm tra học viên đã đăng ký khóa học này chưa.
Đếm số học viên đã đăng ký khóa học.
So sánh với capacity.
Nếu chưa đầy thì tạo bản ghi mới.
Trả về 201 Created.
PHẦN 2: TRIỂN KHAI CODE
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]


class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int


@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(registration: RegistrationCreate):

    # Kiểm tra học viên tồn tại
    student = None
    for s in students:
        if s["id"] == registration.student_id:
            student = s
            break

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Kiểm tra khóa học tồn tại
    course = None
    for c in courses:
        if c["id"] == registration.course_id:
            course = c
            break

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Kiểm tra đăng ký trùng
    for r in registrations:
        if (
            r["student_id"] == registration.student_id
            and r["course_id"] == registration.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student already registered this course"
            )

    # Đếm số lượng đăng ký của khóa học
    count = 0
    for r in registrations:
        if r["course_id"] == registration.course_id:
            count += 1

    # Kiểm tra sĩ số
    if count >= course["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Course is full"
        )

    # Tạo đăng ký mới
    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }

    registrations.append(new_registration)

    return {
        "message": "Registration created successfully",
        "data": new_registration
    }