from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.database import get_read_db
from src.models.product import Product
from src.schemas.product import ProductOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_read_db)) -> list[Product]:
    return list(db.scalars(select(Product).limit(50)))