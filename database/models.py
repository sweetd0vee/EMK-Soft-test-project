import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


class Posts(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)


class Orders(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True)


class Products(Base):
    __tablename__ = "products"


class Customers(Base):
    __tablename__ = "customers"




Base.metadata.create_all(engine)
