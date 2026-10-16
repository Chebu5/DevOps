from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    age: int

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None

class Product(ProductBase):
    id: int
    is_available: bool
    
    class Config:
        from_attributes = True

# Order schemas
class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    total_price: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True