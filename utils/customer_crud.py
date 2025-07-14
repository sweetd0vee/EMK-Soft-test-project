from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Customers
from schemas.models import Customer, DeleteCustomerResponse


def customer_create(db: Session, customer: Customer):
    db_customer = Customers(customer_name=customer.customer_name)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def customers_get_all(db: Session):
    return db.query(Customers).all()


def customer_get_one(db: Session, customer_id: UUID):
    return db.query(Customers).filter_by(customer_id=customer_id).one()


def customer_delete(db: Session, customer_id: UUID):
    customer = db.query(Customers).filter_by(customer_id=customer_id).all()
    if not customer:
        return DeleteCustomerResponse(detail="customer doesn't exist")
    db.query(Customers).filter_by(customer_id=customer_id).delete()
    db.commit()
    return DeleteCustomerResponse(detail="customer deleted")
