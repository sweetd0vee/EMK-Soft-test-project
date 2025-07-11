from uuid import UUID

from sqlalchemy.orm import Session

from database.models import Posts #, Customer, Product, Order
from schemas.models import DeletePostResponse, Post, UpdatePost


def post_create(db: Session, post: Post):
    db_post = Posts(title=post.title, description=post.description)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# def customer_create(db: Session, customer: Customer):
#     db_customer = Customer()
#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)
#     return db_customer


def posts_get_all(db: Session):
    return db.query(Posts).all()


# def orders_get_all(db: Session):
#     return db.query(Orders).all()


def post_get_one(db: Session, id: UUID):
    return db.query(Posts).filter_by(id=id).one()


# def order_get_one(db: Session, customer_id: UUID):
#     return db.query(Orders).filter_by(customer_id=id).one()


def post_update(db: Session, post: UpdatePost):
    update_query = {Posts.title: post.title, Posts.description: post.description}
    db.query(Posts).filter_by(id=post.id).update(update_query)
    db.commit()
    return db.query(Posts).filter_by(id=post.id).one()


def post_delete(db: Session, id: UUID):
    post = db.query(Posts).filter_by(id=id).all()
    if not post:
        return DeletePostResponse(detail="Doesnt Exist")
    db.query(Posts).filter_by(id=id).delete()
    db.commit()
    return DeletePostResponse(detail="Post Deleted")
