import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.utils.other.logger_utils import logger
from fastapi.responses import JSONResponse

from backend.api import router as backend_router
from frontend.routers import router as frontend_router

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")

app = FastAPI()
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="static")
app.include_router(backend_router)
app.include_router(frontend_router)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Необработанное исключение: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Произошла ошибка на сервере."}
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    if request.url.path.startswith("/api") and 300 >= response.status_code >= 400:
        logger.info(f"{request.method} {request.url.path} - Статус: {response.status_code}")

    return response
