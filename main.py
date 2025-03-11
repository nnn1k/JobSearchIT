import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.core.config.cors import setup_cors
from backend.core.utils.logger_utils.exception_log_func import global_exception_handler, log_requests

from backend.api import router as backend_router
from frontend.routers import router as frontend_router

app = FastAPI()

app.include_router(backend_router)
app.include_router(frontend_router)

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="static")

setup_cors(app)

app.exception_handler(Exception)(global_exception_handler)
app.middleware("http")(log_requests)

