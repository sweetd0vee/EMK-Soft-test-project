import uuid

from sqlalchemy import Column, DateTime, DECIMAL, Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)


class Products(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_name = Column(String)
    category = Column(String)
    price = Column(DECIMAL)


class Customers(Base):
    __tablename__ = "customers"

    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.customer_id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
    order_date = Column(DateTime)
    quantity = Column(Integer)


Base.metadata.create_all(engine)
