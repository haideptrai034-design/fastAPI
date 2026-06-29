from fastapi import FastAPI

app = FastAPI()

# Giả lập danh sách sinh viên ban đầu
students = ["An", "Binh", "Cuong"]


# =================================================================
# PHẦN 1: PHÂN TÍCH LỖI (BÀI TẬP 1 & 2)
# =================================================================
#
# 1. Endpoint cũ trong source code là gì?
#    --> Trả lời: Khai báo sai là GET /student (thiếu chữ 's' và tên hàm là create_student).
#
# 2. Vì sao khi gọi GET /students lại bị lỗi 404 Not Found?
#    --> Trả lời: Vì trong code cũ chỉ cài đặt đường dẫn "/student" (số ít). 
#                 Hệ thống không tìm thấy đường dẫn "/students" (số nhiều) nên báo lỗi 404.
#
# 3. Vì sao tên endpoint /student và tên hàm create_student chưa phù hợp?
#    --> Trả lời: - Về endpoint: Lấy "danh sách" (nhiều người) thì chuẩn REST phải dùng số nhiều (/students).
#                 - Về tên hàm: Hàm dùng để LẤY dữ liệu (GET) nhưng lại đặt tên là 'create' (TẠO) 
#                   làm lập trình viên khác và tester bị hiểu nhầm nghiệp vụ.
#
# 4. Vì sao dòng 'return students[0]' chưa đúng với yêu cầu nghiệp vụ?
#    --> Trả lời: Vì students[0] chỉ lấy ra đúng 1 người đầu tiên (bạn "An"), 
#                 trong khi khách hàng yêu cầu lấy "toàn bộ danh sách".
#
# 5. API đúng theo yêu cầu khách hàng nên có đường dẫn là gì?
#    --> Trả lời: GET /students
#
# =================================================================


# =================================================================
# PHẦN 2: SỬA LỖI (MÃ NGUỒN CHUẨN)
# =================================================================

# Chỗ sửa 1: Sửa thành số nhiều "/students" theo đúng yêu cầu khách hàng
@app.get("/students")
# Chỗ sửa 2: Sửa tên hàm thành "get_all_students" cho rõ nghĩa, không để 'create_student' nữa
def get_all_students():
    
    # Chỗ sửa 3: Xóa bỏ '[0]', chỉ return về 'students' để lấy hết cả danh sách
    return students

# =================================================================