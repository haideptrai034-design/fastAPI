"""
Phần 1: Chỉ ra lỗi bằng test case
STT	Dữ liệu gửi lên	Kết quả hiện tại	Kết quả đúng mong muốn	Lỗi phát hiện
1	student_id = "SV001", course_id = 1	API vẫn tạo bản ghi đăng ký mới	API phải báo lỗi vì học viên đã đăng ký khóa học này	Không kiểm tra đăng ký trùng
2	student_id = "SV002", course_id = 1	API vẫn tạo bản ghi đăng ký mới	API phải báo lỗi vì học viên đã đăng ký khóa học này	Cho phép đăng ký cùng một khóa học nhiều lần
Ví dụ Request Test Case 1
POST /enrollments

{
    "student_id": "SV001",
    "course_id": 1
}
Kết quả hiện tại
{
    "message": "Enroll successfully",
    "data": {
        "id": 3,
        "student_id": "SV001",
        "course_id": 1
    }
}

➡ Sai vì học viên SV001 đã đăng ký khóa học 1.

Ví dụ Request Test Case 2
POST /enrollments

{
    "student_id": "SV002",
    "course_id": 1
}
Kết quả hiện tại
{
    "message": "Enroll successfully",
    "data": {
        "id": 3,
        "student_id": "SV002",
        "course_id": 1
    }
}

➡ Sai vì học viên SV002 đã đăng ký khóa học 1.

Phần 2: Sửa source code
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]


class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int


@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):

    # Kiểm tra học viên đã đăng ký khóa học này chưa
    for e in enrollments:
        if (
            e["student_id"] == enrollment.student_id
            and e["course_id"] == enrollment.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student has already enrolled in this course"
            )

    # Tạo đăng ký mới
    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    enrollments.append(new_enrollment)

    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }