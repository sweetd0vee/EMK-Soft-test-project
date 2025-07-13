from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import DeleteOrderResponse, Order, UpdateOrder
from utils.order_crud import (
     order_create,
     order_delete
    # order_get_one,
    # order_update,
    # order_get_all,
)

router_orders = APIRouter(tags=["orders"])


@router_orders.post("/create", status_code=status.HTTP_201_CREATED, response_model=Order)
def create_order(order: Order, db: Session = Depends(get_db)):
    return order_create(db=db, order=order)


# @router_orders.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Post])
# def get_all_posts(db: Session = Depends(get_db)):
#     return posts_get_all(db=db)
#
#
# @router_orders.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=Post)
# def get_one_post(id, db: Session = Depends(get_db)):
#     return post_get_one(db=db, id=id)
#
#
# @router_orders.delete(
#     "/delete/{id}", status_code=status.HTTP_200_OK, response_model=DeletePostResponse
# )
# def delete_post(id, db: Session = Depends(get_db)):
#     delete_status = post_delete(db=db, id=id)
#     if delete_status.detail == "Doesnt Exist":
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found"
#         )
#     else:
#         return delete_status
#
#
# @router_orders.patch("/update", status_code=status.HTTP_200_OK, response_model=Post)
# def update_post(post: UpdatePost, db: Session = Depends(get_db)):
#     return order_update_update(db=db, post=post)


#
# from typing import List
#
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
#
# from database.connection import get_db
# from schemas.models import DeletePostResponse, Post, UpdatePost
# from utils.post_crud import (
#     post_create,
#     post_delete,
#     post_get_one,
#     post_update,
#     posts_get_all,
# )
#
# router_posts = APIRouter(tags=["posts"])
#
#
# @router_posts.post("/create", status_code=status.HTTP_201_CREATED, response_model=Post)
# def create_post(post: Post, db: Session = Depends(get_db)):
#     return post_create(db=db, post=post)
#
#
# @router_posts.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Post])
# def get_all_posts(db: Session = Depends(get_db)):
#     return posts_get_all(db=db)
#
#
# @router_posts.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=Post)
# def get_one_post(id, db: Session = Depends(get_db)):
#     return post_get_one(db=db, id=id)
#
#
# @router_posts.delete(
#     "/delete/{id}", status_code=status.HTTP_200_OK, response_model=DeletePostResponse
# )
# def delete_post(id, db: Session = Depends(get_db)):
#     delete_status = post_delete(db=db, id=id)
#     if delete_status.detail == "Doesnt Exist":
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found"
#         )
#     else:
#         return delete_status
#
#
# @router_posts.patch("/update", status_code=status.HTTP_200_OK, response_model=Post)
# def update_post(post: UpdatePost, db: Session = Depends(get_db)):
#     return post_update(db=db, post=post)
