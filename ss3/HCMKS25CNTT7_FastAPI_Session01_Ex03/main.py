from fastapi import FastAPI

app = FastAPI()

# Danh sách sinh viên ban đầu hệ thống cung cấp
students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]


# =================================================================
# PHẦN 1: BÁO CÁO PHÂN TÍCH NGHIỆP VỤ
# =================================================================
#
# 1. Input của bài toán là gì?
#    --> Trả lời: Danh sách mảng các object sinh viên (biến 'students'), 
#                 mỗi sinh viên gồm các trường: id, name, status.
#
# 2. Output mong muốn là gì?
#    --> Trả lời: Một đối tượng JSON có cấu trúc rõ ràng gồm hai trường:
#                 - "message": Chuỗi thông báo trạng thái.
#                 - "data": Mảng chứa danh sách các sinh viên thỏa mãn điều kiện.
#
# 3. Điều kiện nào dùng để xác định sinh viên đang học?
#    --> Trả lời: Thuộc tính status của sinh viên phải bằng đúng chuỗi "active" 
#                 (tức là: student["status"] == "active").
#
# 4. Các bước xử lý API GET /students/active:
#    - Bước 1: Khởi tạo một mảng rỗng tên là 'active_students' để lưu kết quả lọc.
#    - Bước 2: Sử dụng vòng lặp 'for' để duyệt qua từng sinh viên trong mảng 'students' gốc.
#    - Bước 3: Sử dụng câu lệnh điều kiện 'if' để kiểm tra status của từng sinh viên. 
#              Nếu status == "active", tiến hành append (thêm) sinh viên đó vào mảng 'active_students'.
#    - Bước 4: Kiểm tra số lượng phần tử trong mảng 'active_students' sau khi lọc bằng hàm len():
#              + Nếu len == 0 (bẫy dữ liệu trống): Trả về message "Không có sinh viên đang học" và data [].
#              + Nếu len > 0: Trả về message "Danh sách sinh viên đang học" và data chứa các sinh viên đã lọc.
#
# =================================================================


# =================================================================
# PHẦN 2: TRIỂN KHAI CODE API
# =================================================================

# Định nghĩa chính xác phương thức GET và endpoint /students/active theo yêu cầu
@app.get("/students/active")
def get_active_students():
    # Bước 1: Tạo danh sách chứa kết quả lọc
    active_students = []
    
    # Bước 2 & Bước 3: Duyệt danh sách dữ liệu có sẵn và lọc ra các phần tử thỏa mãn điều kiện
    for student in students:
        if student["status"] == "active":
            active_students.append(student)
            
    # Bước 4: Xử lý ràng buộc & bẫy dữ liệu (Trường hợp không có sinh viên nào đang học)
    if len(active_students) == 0:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }
        
    # Trả về dữ liệu theo cấu trúc rõ ràng gồm message và data khi tìm thấy kết quả
    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }

# =================================================================