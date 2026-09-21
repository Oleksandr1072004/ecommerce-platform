"""Product business logic with cache-aside pattern."""

import json
import logging
from decimal import Decimal

import redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.redis_client import redis_client
from src.models.product import Product
from src.schemas.product import ProductOut

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 300
CACHE_PREFIX = "product"


class ProductService:
    """Service layer for product-related operations.

    Read paths use a cache-aside strategy with Redis:
      1. Try to read from cache.
      2. On miss, read from the DB (replica) and store in cache.
      3. On writes, invalidate related cache keys.
    """

    def __init__(self, db: Session, cache: redis.Redis = redis_client) -> None:
        self.db = db
        self.cache = cache

    # ---------- Helpers ----------

    @staticmethod
    def _key(product_id: int) -> str:
        return f"{CACHE_PREFIX}:{product_id}"

    def _cache_get(self, product_id: int) -> ProductOut | None:
        raw = self.cache.get(self._key(product_id))
        if raw is None:
            return None
        try:
            return ProductOut.model_validate_json(raw)
        except Exception:  # noqa: BLE001
            logger.warning("Failed to decode cached product %s", product_id)
            self.cache.delete(self._key(product_id))
            return None

    def _cache_set(self, product: Product) -> None:
        payload = ProductOut.model_validate(product).model_dump_json()
        self.cache.setex(self._key(product.id), CACHE_TTL_SECONDS, payload)

    def _cache_invalidate(self, product_id: int) -> None:
        self.cache.delete(self._key(product_id))

    # ---------- Read operations ----------

    def list_products(self, limit: int = 50, offset: int = 0) -> list[Product]:
        stmt = select(Product).order_by(Product.id).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def get_product(self, product_id: int) -> ProductOut | None:
        """Fetch one product using cache-aside."""
        cached = self._cache_get(product_id)
        if cached is not None:
            logger.debug("Cache HIT for product %s", product_id)
            return cached

        logger.debug("Cache MISS for product %s", product_id)
        product = self.db.get(Product, product_id)
        if product is None:
            return None

        self._cache_set(product)
        return ProductOut.model_validate(product)

    def search_products(self, query: str, limit: int = 50) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.name.ilike(f"%{query}%"))
            .order_by(Product.id)
            .limit(limit)
        )
        return list(self.db.scalars(stmt))

    # ---------- Write operations ----------

    def create_product(
        self,
        *,
        name: str,
        price: Decimal,
        description: str | None = None,
        stock: int = 0,
    ) -> Product:
        product = Product(
            name=name,
            price=price,
            description=description,
            stock=stock,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_stock(self, product_id: int, delta: int) -> Product | None:
        """Adjust stock and invalidate cache."""
        product = self.db.get(Product, product_id)
        if product is None:
            return None

        product.stock = max(0, product.stock + delta)
        self.db.commit()
        self.db.refresh(product)

        self._cache_invalidate(product_id)
        return product
