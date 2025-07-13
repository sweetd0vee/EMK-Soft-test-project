from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Orders
from schemas.models import DeleteOrderResponse, Order
# from schemas.models import UpdateOrder


def order_create(db: Session, order: Order):
    db_post = Orders(order_date=order.order_date,
                     product_id=order.product_id,
                     customer_id=order.customer_id,
                     quntity=order.quantity)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def orders_get_all(db: Session):
    return db.query(Orders).all()


# все заказы по дате
def order_get_all_date(db:Session, order_date):
    return db.query(Orders).filter_by(order_date=order_date).all()


# все заказы по customer_id
def order_get_all_customer(db: Session, customer_id):
    return db.query(Orders).filter_by(customer_id=customer_id).all()

def order_get_one_id(db: Session, id: UUID):
    return db.query(Orders).filter_by(id=id).one()


def order_get_one_(db: Session, id: UUID):
    return db.query(Orders).filter_by(id=id).one()


# def order_update(db: Session, order: UpdateOrder):
#     update_query = {
#         Orders.order_date: order.order_date,
#         Orders.product_id: order.product_id,
#         Orders.customer_id: order.customer_id,
#         Orders.quntity: order.quantity
#     }
#     db.query(Orders).filter_by(id=order.id).update(update_query)
#     db.commit()
#     return db.query(Orders).filter_by(id=order.id).one()


def order_delete(db: Session, id: UUID):
    order = db.query(Orders).filter_by(id=id).all()
    if not order:
        return DeleteOrderResponse(detail="Order doesn't exist")
    db.query(Orders).filter_by(id=id).delete()
    db.commit()
    return DeleteOderResponse(detail="Order deleted")
