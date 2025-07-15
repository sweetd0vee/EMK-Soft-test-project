from database.connection import Base, engine

from sqlalchemy import Column, DateTime, DECIMAL, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func

import uuid


class Customers(Base):
    __tablename__ = "customers"

    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    customer_name = Column(String, nullable=False)
    orders = relationship("Orders", back_populates="customer")


class Products(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    orders = relationship("Orders", back_populates="product")


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    order_date = Column(DateTime, nullable=False, server_default=func.now())
    quantity = Column(Integer, nullable=False)
    customer = relationship("Customers", back_populates="orders")
    product = relationship("Products", back_populates="orders")


Base.metadata.create_all(engine)
