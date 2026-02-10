from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers 

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
