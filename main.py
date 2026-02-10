from fastapi import FastAPI
from app.models import User, Product, Cart, CartItem, Order, OrderItem
# from app.routers 

app = FastAPI(
    title="Mini E-Commerce API",
    version="1.0",
    description="Mini E-Commerce API | AppifyDevs | Mirza Salem | 2026",
)

@app.get("/")
def root():
    return {
        "message": "Mini E-Commerce API",
        "Owner": "Mirza Salem",
        "Git_link": "https://github.com/mirzasalem"
    }
