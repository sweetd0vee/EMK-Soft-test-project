from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import DeleteOrderResponse, Order, UpdateOrder
from utils.order_crud import (
     order_create,
     orders_get_all,
     order_get_one,
     order_delete,
     order_update,
     order_get_all_customer
)

# order_create, orders_get_all, order_delete, order_update, order_get_one, order_get_all_customer


router_orders = APIRouter(tags=["orders"])


@router_orders.post("/create", status_code=status.HTTP_201_CREATED, response_model=Order)
def create_order(order: Order, db: Session = Depends(get_db)):
    return order_create(db=db, order=order)


@router_orders.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Order])
def get_all_orders(db: Session = Depends(get_db)):
    return orders_get_all(db=db)


@router_orders.delete(
    "/delete/{id}", status_code=status.HTTP_200_OK, response_model=DeleteOrderResponse
)
def delete_order(id, db: Session = Depends(get_db)):
    delete_status = order_delete(db=db, id=id)
    if delete_status.detail == "Order doesn't exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    else:
        return delete_status


@router_orders.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=Order)
def get_one_order(id, db: Session = Depends(get_db)):
    return order_get_one(db=db, id=id)


@router_orders.patch("/update", status_code=status.HTTP_200_OK, response_model=Order)
def update_order(order: UpdateOrder, db: Session = Depends(get_db)):
    return order_update(db=db, order=order)


@router_orders.get("/get/{customer_id}", status_code=status.HTTP_200_OK, response_model=Order)
def get_one_order(customer_id, db: Session = Depends(get_db)):
    return order_get_all_customer(db=db, customer_id=customer_id)
