# phân tích:
# Frontend (Client)
#         │
#         │ Gửi HTTP GET /getStudents
#         ▼
# FastAPI nhận request
#         │
#         ▼
# Tìm Route:
# @app.get("/getStudents")
#         │
#         ▼
# Thực thi hàm:
# get_students()
#         │
#         ▼
# Hàm lấy dữ liệu:
# students = ["An", "Binh", "Cuong"]
#         │
#         ▼
# return "Danh sach sinh vien: " + str(students)
#         │
#         ▼
# Server trả về String cho Frontend


# Frontend thường cần một JSON Array để có thể duyệt từng sinh viên và hiển thị lên giao diện. Nếu API trả về String thì Frontend sẽ không xử lý dữ liệu đúng cách.

# Endpoint /getStudents chưa đúng chuẩn REST vì có động từ get. Nên đổi thành /students.

from fastapi import FastAPI

app = FastAPI()

students = ["An", "Binh", "Cuong"]

@app.get("/students")
def get_students():
    return students