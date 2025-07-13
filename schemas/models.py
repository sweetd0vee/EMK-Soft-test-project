from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class Post(BaseModel):
    id: Optional[UUID]
    title: str
    description: str

    class Config:
        orm_mode = True


class DeletePostResponse(BaseModel):
    detail: str


class UpdatePost(BaseModel):
    id: UUID
    title: str
    description: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    Product_id: Optional[UUID] # PK
    Product_name: str
    Category: str
    Price: float #double


class DeleteProductResponse(BaseModel):
    description: str


class Customer(BaseModel):
    id: Optional[UUID]         # PK
    Name: str


class DeleteCustomerResponse(BaseModel):
    detail: str


class Order(BaseModel):
    Order_id: Optional[UUID]    # PK
    Order_date: datetime
    Customer_id: UUID           # FK
    Product_id: UUID            # FK
    Quantity: int


class DeleteOrderResponse(BaseModel):
    detail: str

