from base_logger import logger
from database.models import Orders

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from schemas.models import DeleteOrderResponse, Order, UpdateOrder, OrdersSearchFilter

from typing import List
from uuid import UUID


# order_create, orders_get_all, order_delete, order_update, order_get_one, order_get_all_customer
def order_create(db: Session, order: Order):
    """
    Create a new order record in the database.

    :param db: SQLAlchemy Session
    :param order: Order data to create
    :return: The created Order instance
    """
    db_order = Orders(
        order_date=order.order_date,
        product_id=order.product_id,
        customer_id=order.customer_id,
        quantity=order.quantity
    )
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        logger.info("Saved order with order_id = ", db_order.order_id)
        return db_order
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Failed to save order: %s", e, exc_info=True)
        raise


def orders_get_all(db: Session) -> List[Orders]:
    """
    Retrieve all orders from the Orders table.

    :param db: SQLAlchemy Session
    :return: List of Orders instances
    """
    return db.query(Orders).all()


def order_delete(db: Session, order_id: UUID):
    """
    Delete order with order_id if it exists.

    :param db: SQLAlchemy Session
    :param order_id: UUID of the order to delete
    :return: DeleteOrderResponse
    """
    order = db.query(Orders).filter_by(order_id=order_id).first()
    if not order:
        return DeleteOrderResponse(detail="Order doesn't exist")
    db.query(Orders).filter_by(order_id=order_id).delete()
    db.commit()
    return DeleteOrderResponse(detail="Order deleted")


def order_update(db: Session, order: UpdateOrder):
    """
    Updates order in orders database with new UpdateOrder params.

    :param db: SQLAlchemy Session
    :param order: UpdateOrder object
    :return: Updated order object
    """
    update_query = {
        Orders.order_date: order.order_date,
        Orders.product_id: order.product_id,
        Orders.customer_id: order.customer_id,
        Orders.quantity: order.quantity
    }
    db.query(Orders).filter_by(order_id=order.order_id).update(update_query)
    db.commit()
    return db.query(Orders).filter_by(order_id=order.order_id).one()


def order_get_one(db: Session, order_id: UUID):
    """
    Return the order object with passed UUID order_id.

    :param db: SQLAlchemy Session object to interact with the database
    :param order_id: UUID of the order to retrieve
    :return: The order object matching the given order_id
    """
    return db.query(Orders).filter_by(order_id=order_id).one()


def orders_get_by_customer(db: Session, customer_id: UUID):
    """
        Return the order object with passed UUID order_id.

        :param db: SQLAlchemy Session object to interact with the database
        :param customer_id: UUID of the customer_id whose orders to retrieve
        :return: The order objects matching the given order_id
    """
    return db.query(Orders).filter_by(customer_id=customer_id).all()


def orders_search(db: Session, filter: OrdersSearchFilter):
    """
    Search orders based on optional filter criteria.

    :param db: SQLAlchemy Session
    :param filter: OrdersSearchFilter instance with optional search parameters
    :return: List of Orders matching the filter criteria
    """
    query = db.query(Orders)
    if filter.order_id:
        query = query.filter_by(order_id=filter.order_id)
    if filter.product_id:
        query = query.filter_by(product_id=filter.product_id)
    if filter.customer_id:
        query = query.filter_by(customer_id=filter.customer_id)
    if filter.quantity:
        query = query.filter_by(quantity=filter.quantity)
    return query.all()

