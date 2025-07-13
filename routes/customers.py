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

router = APIRouter(tags=["customers"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    return customer_create(db=db, customer=customer)


@router.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Customer])
def get_all_customers(db: Session = Depends(get_db)):
    return customers_get_all(db=db)


@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=Customer)
def get_one_customer(id, db: Session = Depends(get_db)):
    return customer_get_one(db=db, id=id)


@router.delete(
    "/delete/{id}", status_code=status.HTTP_200_OK, response_model=DeleteCustomerResponse
)
def delete_customer(id, db: Session = Depends(get_db)):
    delete_status = customer_delete(db=db, id=id)
    if delete_status.detail == "customer doesn't exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="customer not found"
        )
    else:
        return delete_status
