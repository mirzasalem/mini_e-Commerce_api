from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.order import OrderStatus
from app.schemas.product import ProductResponse


 


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product: ProductResponse
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: OrderStatus
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    
    
# class OrderCreate(BaseModel):
#     pass 