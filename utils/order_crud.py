from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Orders
from schemas.models import DeleteOrderResponse, Order, UpdateOrder, OrdersSearchFilter


# order_create, orders_get_all, order_delete, order_update, order_get_one, order_get_all_customer
def order_create(db: Session, order: Order):
    db_post = Orders(
        order_date=order.order_date,
        product_id=order.product_id,
        customer_id=order.customer_id,
        quantity=order.quantity
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def orders_get_all(db: Session):
    return db.query(Orders).all()


def order_delete(db: Session, order_id: UUID):
    order = db.query(Orders).filter_by(order_id=order_id).all()
    if not order:
        return DeleteOrderResponse(detail="order doesn't exist")
    db.query(Orders).filter_by(order_id=order_id).delete()
    db.commit()
    return DeleteOrderResponse(detail="order deleted")


def order_update(db: Session, order: UpdateOrder):
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
    return db.query(Orders).filter_by(order_id=order_id).one()


def orders_search(db: Session, filter: OrdersSearchFilter):
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

