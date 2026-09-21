from fastapi import FastAPI

from src.api.v1 import health, products
from src.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(health.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.app_name, "docs": "/docs"}