from base_logger import logger

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import DeleteOrderResponse, Order, UpdateOrder, OrdersSearchFilter
from utils.order_crud import (
     order_create,
     orders_get_all,
     order_get_one,
     orders_get_by_customer,
     order_delete,
     order_update,
     orders_search
)


router_orders = APIRouter(tags=["orders"])


@router_orders.post("", status_code=status.HTTP_201_CREATED, response_model=Order)
def create_order(order: Order, db: Session = Depends(get_db)):
    """
    Create a new order.

    :param order: Order data to create, validated by Pydantic model `Order`
    :param db: SQLAlchemy Session
    :return: The created order instance
    :raises HTTPException: If order creation fails due to internal error
    """
    logger.info("Call order create endpoint with arguments: %s", order)
    try:
        created_order = order_create(db=db, order=order)
        return created_order
    except Exception as e:
        logger.error("Failed to create order: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create order")


@router_orders.get("", status_code=status.HTTP_200_OK, response_model=List[Order])
def get_all_orders(db: Session = Depends(get_db)):
    """
        Retrieve all orders from the database.
    """
    logger.info("Call get all orders endpoint")
    try:
        return orders_get_all(db=db)
    except Exception as e:
        logger.error("Failed to retrieve all orders: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders"
        )


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


@router_customers.get("/customer_id", status_code=status.HTTP_200_OK, response_model=List[Order])
def get_orders_by_customer(customer_id, db: Session = Depends(get_db)):
    """
    Retrieve a list of all orders with customer_id.

    :param: customer_id: UUID of the customer whose orders are to be fetched.
    :param: db (Session): SQLAlchemy database session.
    :return: List[Order]: A list of all order records.
    :raises: HTTPException: 404 if the customer or orders are not found.
             HTTPException: 500 if the database retrieval fails.
    """
    logger.info(f"Fetching orders for customer with ID: {customer_id}")
    try:
        orders = orders_get_by_customer(db=db, customer_id=customer_id)  # Implement this helper function
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this customer")
        logger.info(f"Found {len(orders)} orders for customer {customer_id}")
        return orders

    except HTTPException:  # Re-raise HTTP exceptions for 404
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve orders for customer {customer_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve orders")


@router_orders.post("/search", status_code=status.HTTP_200_OK, response_model=List[Order])
def search_orders(filter: OrdersSearchFilter, db: Session = Depends(get_db)):
    """
    Search for orders based on provided filter criteria.

    :param filter (OrdersSearchFilter): Filtering criteria for searching orders.
    :param db (Session): Database session dependency.
    :return: List[Order]: List of orders matching the given filter.
    :raises: HTTPException: When search fails due to internal error.
    """
    logger.info("Search orders called with filter: %s", filter)
    try:
        results = orders_search(db=db, filter=filter)
        return results
    except Exception as e:
        logger.error("Failed to search orders: %s", e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to search orders")
