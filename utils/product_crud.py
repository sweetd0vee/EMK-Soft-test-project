from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Products
from schemas.models import Product, DeleteProductResponse


def product_create(db: Session, product: Product):
    db_product = Products(
        product_name=product.product_name,
        category=product.category,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def product_get_all(db: Session):
    return db.query(Products).all()


def product_get_one(db: Session, product_id: UUID):
    return db.query(Products).filter_by(product_id=product_id).one()


def product_delete(db: Session, product_id: UUID):
    customer = db.query(Products).filter_by(product_id=product_id).all()
    if not customer:
        return DeleteProductResponse(detail="product doesn't exist")
    db.query(Products).filter_by(product_id=product_id).delete()
    db.commit()
    return DeleteProductResponse(detail="product deleted")
