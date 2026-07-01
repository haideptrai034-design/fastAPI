from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ======================
# Dữ liệu mẫu
# ======================

students = [
    {
        "id": 1,
        "code": "SV001",
        "name": "Nguyen Van A",
        "email": "a@gmail.com",
        "age": 20
    },
    {
        "id": 2,
        "code": "SV002",
        "name": "Tran Thi B",
        "email": "b@gmail.com",
        "age": 22
    },
    {
        "id": 3,
        "code": "SV003",
        "name": "Le Van C",
        "email": "c@gmail.com",
        "age": 18
    }
]

# ======================
# Model
# ======================

class Student(BaseModel):
    code: str
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)

# ======================
# POST - Thêm học viên
# ======================

@app.post("/students")
def create_student(student: Student):

    # Kiểm tra code trùng
    for item in students:
        if item["code"].lower() == student.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Student code already exists"
            )

    new_student = {
        "id": max(s["id"] for s in students) + 1 if students else 1,
        **student.model_dump()
    }

    students.append(new_student)

    return {
        "message": "Student created successfully",
        "data": new_student
    }

# ======================
# GET - Danh sách học viên
# Có tìm kiếm và lọc
# ======================

@app.get("/students")
def get_students(
    keyword: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None
):

    result = students

    if keyword:
        result = [
            s for s in result
            if keyword.lower() in s["name"].lower()
            or keyword.lower() in s["code"].lower()
            or keyword.lower() in s["email"].lower()
        ]

    if min_age is not None:
        result = [
            s for s in result
            if s["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            s for s in result
            if s["age"] <= max_age
        ]

    return result

# ======================
# GET - Chi tiết học viên
# ======================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

# ======================
# PUT - Cập nhật học viên
# ======================

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            # Kiểm tra code trùng
            for item in students:
                if (
                    item["id"] != student_id
                    and item["code"].lower() == updated_student.code.lower()
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Student code already exists"
                    )

            students[index] = {
                "id": student_id,
                **updated_student.model_dump()
            }

            return {
                "message": "Student updated successfully",
                "data": students[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

# ======================
# DELETE - Xóa học viên
# ======================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:
            deleted = students.pop(index)

            return {
                "message": "Student deleted successfully",
                "data": deleted
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )