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
    product_id: Optional[UUID]
    product_name: str
    category: str
    price: float


class DeleteProductResponse(BaseModel):
    description: str


class Customer(BaseModel):
    id: Optional[UUID]
    customer_name: str


class DeleteCustomerResponse(BaseModel):
    detail: str


class Order(BaseModel):
    order_id: Optional[UUID]
    order_date: datetime
    customer_id: UUID
    product_id: UUID
    quantity: int


class UpdateOrder(BaseModel):
    order_id: UUID
    order_date: datetime
    customer_id: UUID
    product_id: UUID
    quantity: int


class DeleteOrderResponse(BaseModel):
    detail: str

