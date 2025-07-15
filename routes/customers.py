from base_logger import logger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import Customer, DeleteCustomerResponse
from utils.customer_crud import (
    customer_create,
    customer_get_one,
    customers_get_all,
    customer_delete
)

router_customers = APIRouter(tags=["customers"])


@router_customers.post("", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    """
    Create a new customer.

    :param customer: Customer data to create, validated by Pydantic model `Customer`.
    :param db: SQLAlchemy Session.
    :return: The created customer instance.
    :raises HTTPException: If customer creation fails due to internal error.
    """
    logger.info("Call customer create endpoint with arguments: %s", customer)
    try:
        new_customer = customer_create(db=db, customer=customer)
        logger.info(f"Successfully created customer with ID: {new_customer.customer_id}")
        return new_customer
    except Exception as e:
        logger.error("Failed to create customer: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create customer")


@router_customers.get("", status_code=status.HTTP_200_OK, response_model=List[Customer])
def get_all_customers(db: Session = Depends(get_db)):
    """
    Retrieve a list of all customers.

    :param:  db (Session): SQLAlchemy database session.
    :return: List[Customer]: A list of all customer records.
    """
    logger.info("Call get all customers endpoint")
    try:
        return customers_get_all(db=db)
    except Exception as e:
        logger.error("Failed to retrieve customers: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve customers")


@router_customers.get("/{customer_id}", status_code=status.HTTP_200_OK, response_model=Customer)
def get_one_customer(customer_id, db: Session = Depends(get_db)):
    """
    Retrieve a customer by their unique ID.

    :param customer_id: UUID of the customer to retrieve.
    :param db: SQLAlchemy Session.
    :return: The customer data.
    :raises HTTPException: 404 if customer not found.
    """
    logger.info(f"Fetching customer with ID: {customer_id}")
    customer = customer_get_one(db=db, customer_id=customer_id)
    if not customer:
        logger.warning(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router_customers.delete(
    "/{customer_id}", status_code=status.HTTP_200_OK, response_model=DeleteCustomerResponse
)
def delete_customer(customer_id, db: Session = Depends(get_db)):
    """
    Delete a customer by ID.

    :param customer_id: The UUID of the customer to delete.
    :param db: SQLAlchemy Session
    :return: dict: Deletion confirmation or details.
    :raises: HTTPException: 404 if customer does not exist.
    """
    logger.info("Attempting to delete customer with ID: %s", customer_id)
    delete_status = customer_delete(db=db, customer_id=customer_id)

    if delete_status.detail == "Customer doesn't exist":
        logger.warning("Customer with ID %s not found", customer_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    logger.info("Successfully deleted customer with ID: %s", customer_id)
    return delete_status
