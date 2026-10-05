import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Never leak stack traces to users in sandbox/production."""
    logger.exception("Unhandled error on %s", request.url.path)

    detail = "Internal server error"
    if settings.show_error_details:  # dev/sandbox only
        detail = f"{type(exc).__name__}: {exc}"

    return JSONResponse(status_code=500, content={"detail": detail})