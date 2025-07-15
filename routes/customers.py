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


@router_customers.post("/create", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    """
    Create a new customer.

    :param customer: Customer data to create, validated by Pydantic model `Customer`
    :param db: SQLAlchemy Session
    :return: The created customer instance
    :raises HTTPException: If customer creation fails due to internal error
    """
    try:
        new_customer = customer_create(db=db, customer=customer)
        return new_customer
    except Exception as e:
        logger.error("Failed to create customer: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create customer")


@router_customers.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Customer])
def get_all_customers(db: Session = Depends(get_db)):
    """

    :param db:
    :return:
    """
    return customers_get_all(db=db)


@router_customers.get("/{customer_id}", status_code=status.HTTP_200_OK, response_model=Customer)
def get_one_customer(customer_id, db: Session = Depends(get_db)):
    return customer_get_one(db=db, customer_id=customer_id)


@router_customers.delete(
    "/{customer_id}", status_code=status.HTTP_200_OK, response_model=DeleteCustomerResponse
)
def delete_customer(customer_id, db: Session = Depends(get_db)):
    delete_status = customer_delete(db=db, customer_id=customer_id)
    if delete_status.detail == "customer doesn't exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="customer not found"
        )
    else:
        return delete_status
