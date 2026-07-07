# Bảng phân tích lỗi
# STT	Hành vi lỗi trong code hiện tại	Hậu quả đối với Database MySQL	Cách khắc phục bằng SQLAlchemy
# 1	Thiếu lệnh xác thực lưu dữ liệu (db.commit())	Dữ liệu chỉ tồn tại trong Session, không được ghi vào bảng products, sau khi Session kết thúc transaction sẽ bị rollback hoặc hủy	Sau db.add(new_product) gọi db.commit() rồi db.refresh(new_product) nếu cần lấy dữ liệu mới
# 2	Không giải phóng/đóng Session	Connection tới MySQL không được trả về Connection Pool, nhiều request liên tục có thể gây rò rỉ connection, hết pool và làm giảm hiệu năng	Đặt db.close() trong khối finally hoặc sử dụng Dependency Injection (yield) của FastAPI để tự động đóng Session
# Code sửa đúng
from fastapi import FastAPI, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float

app = FastAPI()

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    db = SessionLocal()

    try:
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price
        )

        db.add(new_product)
        db.commit()            # Ghi dữ liệu xuống MySQL
        db.refresh(new_product) # Đồng bộ object với DB

        return {
            "message": "Product created successfully",
            "data": {
                "id": new_product.id,
                "sku": new_product.sku,
                "name": new_product.name,
                "price": new_product.price
            }
        }

    finally:
        db.close()             # Giải phóng Session