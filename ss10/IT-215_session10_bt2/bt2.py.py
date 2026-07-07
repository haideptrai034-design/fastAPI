# STT	Phương thức truy vấn hiện tại	Tình huống gây lỗi (Edge Case)	Phương thức thay thế an toàn hơn
# 1	.one()	Gọi GET /orders/999 khi order_id = 999 không tồn tại trong bảng orders. .one() ném ngoại lệ NoResultFound, làm API trả về 500 Internal Server Error và có thể lộ Stack Trace.	.first() kết hợp kiểm tra None và ném HTTPException(status_code=status.HTTP_404_NOT_FOUND) để trả về 404 Not Found.

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    total_price = Column(Integer)

app = FastAPI()


@app.get("/orders/{order_id}")
def get_order_detail(order_id: int):
    db = SessionLocal()

    try:
        # Truy vấn đơn hàng
        order = db.query(OrderModel).filter(OrderModel.id == order_id).first()

        # Không tìm thấy đơn hàng
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        # Trả về thông tin đơn hàng
        return {
            "id": order.id,
            "customer": order.customer_name,
            "total_price": order.total_price
        }

    finally:
        db.close()