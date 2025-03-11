from fastapi import Request
from fastapi.responses import JSONResponse

from backend.core.utils.logger_utils.logger_func import logger

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Необработанное исключение: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Произошла ошибка на сервере."}
    )

async def log_requests(request: Request, call_next):
    response = await call_next(request)

    if request.url.path.startswith("/api"):
        logger.info(f"{request.method} {request.url.path} - Статус: {response.status_code}")

    return response
