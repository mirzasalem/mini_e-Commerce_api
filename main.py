from fastapi import FastAPI
from app.core.database import engine
from app.models import Base
import os
from app.routers import auth, products, cart, orders
from fastapi.staticfiles import StaticFiles
app = FastAPI(
    title="Mini E-Commerce API",
    version="1.0",
    description="Mini E-Commerce API | AppifyDevs | Mirza Salem | 2026",
    )

# app.mount("/static", StaticFiles(directory="static"), name="static")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)
# Create all tables
Base.metadata.create_all(bind=engine)


# For included routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])


@app.get("/")
def root():
    return {
        "message": "Mini E-Commerce API",
        "Owner": "Mirza Salem",
        "Project Link": "https://github.com/mirzasalem/mini_e-Commerce_api"
    }
