from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.v1 import auth, health, pages, products, users, login_page
from src.core.config import settings
from src.core.database import Base, engine
from src.models import product, user  # noqa: F401 — register models


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.app_env == "dev":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(                                   # <-- all keyword args
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

# (optional) Trusted hosts for Lab №3
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    import logging
    logging.getLogger(__name__).exception("Unhandled error on %s", request.url.path)
    detail = "Internal server error"
    if settings.show_error_details:
        detail = f"{type(exc).__name__}: {exc}"
    return JSONResponse(status_code=500, content={"detail": detail})


app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(pages.router)
app.include_router(login_page.router)

@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.app_name, "docs": "/docs"}