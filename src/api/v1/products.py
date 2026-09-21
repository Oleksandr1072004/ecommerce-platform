from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.core.database import get_db, get_read_db
from src.schemas.product import ProductCreate, ProductOut
from src.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_read_db),
) -> list[ProductOut]:
    return ProductService(db).list_products(limit=limit, offset=offset)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_read_db)) -> ProductOut:
    product = ProductService(db).get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductOut, status_code=201)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductOut:
    product = ProductService(db).create_product(
        name=payload.name,
        price=payload.price,
        description=payload.description,
        stock=payload.stock,
    )
    return ProductOut.model_validate(product)
