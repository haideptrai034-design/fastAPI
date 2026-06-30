# Lỗi xảy ra vì backend khai báo sai Path Parameter.
# "/products/product_id" là đường dẫn cố định, không phải biến.
# Do đó khi gọi "/products/1", hệ thống không match route -> 404.
# Cách sửa: dùng dấu {} -> "/products/{product_id}".
# Khi đó FastAPI sẽ nhận giá trị từ URL và truyền vào hàm.

from fastapi import FastAPI
app = FastAPI()
products=[
    {"id":1,"name":"Laptop Dell","price":15000000},
    {"id":2,"name":"Chuột Logitech","price":350000},
    {"id":3,"name":"Bàn phím cơ","price":1200000}
]
@app.get("/products/{product_id}")
def get_product_detail(product_id:int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {
        "massage":"Không tìm thấy sản phẩm"
    }
