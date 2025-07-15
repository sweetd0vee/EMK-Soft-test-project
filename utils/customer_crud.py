from base_logger import logger
from database.models import Customers

from sqlalchemy.exc import SQLAlchemyError
from schemas.models import Customer, DeleteCustomerResponse
from sqlalchemy.orm import Session

from uuid import UUID


def customer_create(db: Session, customer: Customer):
    """
    Create a new customer record in the database.

    :param db: SQLAlchemy Session
    :param customer: Customer data to create
    :return: The created Customer instance
    """
    db_customer = Customers(customer_name=customer.customer_name)
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        logger.info("Saved customer with customer_id = ", db_customer.customer_id)
        return db_customer
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Failed to save customer: %s", e, exc_info=True)
        # Optionally, re-raise or handle the exception as needed
        raise


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
