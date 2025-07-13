from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import Product, DeleteProductResponse
from utils.product_crud import (
    product_create,
    product_get_all,
    product_delete
)

router = APIRouter(tags=["products"])


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_product(product: Product, db: Session = Depends(get_db)):
    return product_create(db=db, customer=product)


@router.get("/list/all", status_code=status.HTTP_200_OK, response_model=List[Product])
def get_all_products(db: Session = Depends(get_db)):
    return product_get_all(db=db)


@router.delete(
    "/delete/{id}", status_code=status.HTTP_200_OK, response_model=DeleteProductResponse
)
def delete_product(id, db: Session = Depends(get_db)):
    delete_status = product_delete(db=db, id=id)
    if delete_status.detail == "Doesnt Exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found"
        )
    else:
        return delete_status
