# Phần 1. Báo cáo phân tích bài toán
# 1. Phân tích Input/Output
# Input (Pydantic Model)

# API chỉ cho phép người dùng gửi:

# warehouse_code: Mã kho vận
# location: Vị trí kho
# class InventoryRequest(BaseModel):
#     warehouse_code: str
#     location: str
# Output
# Trường hợp thành công (HTTP 201)
# {
#     "message": "Tạo kho vận thành công",
#     "data": {
#         "id": 1,
#         "warehouse_code": "WH-HN-01",
#         "location": "Hà Nội"
#     }
# }
# Trường hợp mã kho đã tồn tại (HTTP 400)
# {
#     "detail": "Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
# }
# 2. Thuật toán xử lý
# Bước 1:
#     Mở kết nối đến MySQL.

# Bước 2:
#     Nhận warehouse_code và location từ request.

# Bước 3:
#     Thực hiện SELECT bằng filter()
#     tìm warehouse_code trong bảng inventories.

# Bước 4:
#     Nếu tìm thấy dữ liệu
#         -> HTTPException(400)
#         -> "Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"

# Bước 5:
#     Nếu chưa tồn tại
#         -> Tạo InventoryModel
#         -> db.add()
#         -> db.commit()
#         -> db.refresh()

# Bước 6:
#     Trả về dữ liệu vừa tạo.

# Bước 7:
#     Đóng Session.
# Phần 2. Triển khai mã nguồn hoàn chỉnh
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class InventoryModel(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True)
    warehouse_code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100), nullable=False)


Base.metadata.create_all(bind=engine)


class InventoryRequest(BaseModel):
    warehouse_code: str
    location: str


app = FastAPI()


@app.post("/inventories", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: InventoryRequest):
    db = SessionLocal()

    try:
        # Kiểm tra warehouse_code đã tồn tại hay chưa
        existing_inventory = (
            db.query(InventoryModel)
            .filter(
                InventoryModel.warehouse_code == inventory.warehouse_code
            )
            .first()
        )

        if existing_inventory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
            )

        # Thêm mới kho vận
        new_inventory = InventoryModel(
            warehouse_code=inventory.warehouse_code,
            location=inventory.location
        )

        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)

        return {
            "message": "Tạo kho vận thành công",
            "data": {
                "id": new_inventory.id,
                "warehouse_code": new_inventory.warehouse_code,
                "location": new_inventory.location
            }
        }

    finally:
        db.close()