from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Products
from schemas.models import Product, DeleteProductResponse


def product_create(db: Session, customer: Product):
    db_customer = Products(name=Product.product_name)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def product_get_all(db: Session):
    return db.query(Products).all()


def product_get_one(db: Session, id: UUID):
    return db.query(Products).filter_by(id=id).one()


def product_delete(db: Session, id: UUID):
    customer = db.query(Products).filter_by(id=id).all()
    if not customer:
        return DeleteProductResponse(detail="Product Doesnt Exist")
    db.query(Products).filter_by(id=id).delete()
    db.commit()
    return DeleteProductResponse(detail="Product Deleted")
