from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class Product(BaseModel):
    product_id: Optional[UUID]
    product_name: str
    category: str
    price: float

    class Config:
        orm_mode = True


class DeleteProductResponse(BaseModel):
    description: str


class Customer(BaseModel):
    id: Optional[UUID]
    customer_name: str

    class Config:
        orm_mode = True


class DeleteCustomerResponse(BaseModel):
    detail: str


class Order(BaseModel):
    order_id: Optional[UUID]
    order_date: datetime
    customer_id: UUID
    product_id: UUID
    quantity: int

    class Config:
        orm_mode = True


class DeleteOrderResponse(BaseModel):
    detail: str


class UpdateOrder(BaseModel):
    order_id: UUID
    order_date: datetime
    customer_id: UUID
    product_id: UUID
    quantity: int

    class Config:
        orm_mode = True


class OrdersSearchFilter(BaseModel):
    order_id: Optional[UUID]
    product_id: Optional[UUID]
    customer_id: Optional[UUID]
    quantity: Optional[int]