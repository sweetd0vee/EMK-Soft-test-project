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


# class Customer(BaseModel):
#     id: UUID # PK
#     Name: str


# class Product(BaseModel):
#     Product_id: UUID # PK
#     Product_name: str
#     Category: str
#     Price: float #double


# class Order(BaseModel):
#     Order_id: UUID # PK
#     Order_date: datetime
#     Customer_id: UUID # FK
#     Product_id: UUID # FK
#     Quantity: int
