from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import Product, DeleteProductResponse
from utils.product_crud import (
    product_create,
    product_get_all,
    product_get_one,
    product_delete
)

router_products = APIRouter(tags=["products"])


@router_products.post("/create", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    return product_create(db=db, product=product)


@router_products.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Product])
def get_all_products(db: Session = Depends(get_db)):
    return product_get_all(db=db)


@router_products.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=Product)
def get_one_customer(product_id, db: Session = Depends(get_db)):
    return product_get_one(db=db, product_id=product_id)


@router_products.delete("/{product_id}", status_code=status.HTTP_200_OK, response_model=DeleteProductResponse)
def delete_product(product_id, db: Session = Depends(get_db)):
    delete_status = product_delete(db=db, product_id=product_id)
    if delete_status.detail == "product doesn't exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="product not found"
        )
    else:
        return delete_status
