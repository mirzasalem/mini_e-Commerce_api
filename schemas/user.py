from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=15) # bcrypt limit
    role: Optional[UserRole] = UserRole.CUSTOMER



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole
    created_at: datetime
    order_cancellation_count: int = 0
    
    class Config:
        from_attributes = True


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse