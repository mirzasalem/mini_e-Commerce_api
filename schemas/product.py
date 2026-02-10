from pydantic import BaseModel, Field, computed_field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def image_url(self) -> Optional[str]:
        if self.image:
            return f"http://localhost:8000/static/products/{self.image}"
        return None
    class Config:
        from_attributes = True
