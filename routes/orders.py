from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import DeleteOrderResponse, Order, UpdateOrder, OrdersSearchFilter
from utils.order_crud import (
     order_create,
     orders_get_all,
     order_get_one,
     order_delete,
     order_update,
     orders_search
)

from base_logger import logger

# order_create, orders_get_all, order_delete, order_update, order_get_one


router_orders = APIRouter(tags=["orders"])


@router_orders.post("/create", status_code=status.HTTP_201_CREATED, response_model=Order)
def create_order(order: Order, db: Session = Depends(get_db)):
    logger.info("Call order create endpoint with arguments: ", order)
    return order_create(db=db, order=order)


@router_orders.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Order])
def get_all_orders(db: Session = Depends(get_db)):

    return orders_get_all(db=db)


@router_orders.delete("/{order_id}", status_code=status.HTTP_200_OK, response_model=DeleteOrderResponse)
def delete_order(order_id, db: Session = Depends(get_db)):
    delete_status = order_delete(db=db, order_id=order_id)
    if delete_status.detail == "order doesn't exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found"
        )
    else:
        return delete_status


@router_orders.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=Order)
def get_one_order(order_id, db: Session = Depends(get_db)):
    return order_get_one(db=db, order_id=order_id)


@router_orders.patch("/update", status_code=status.HTTP_200_OK, response_model=Order)
def update_order(order: UpdateOrder, db: Session = Depends(get_db)):
    return order_update(db=db, order=order)


@router_orders.post("/search", status_code=status.HTTP_200_OK, response_model=List[Order])
def search_orders(filter: OrdersSearchFilter, db: Session = Depends(get_db)):
    return orders_search(db=db, filter=filter)
