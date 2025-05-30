import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from fastapi.responses import JSONResponse

from backend.core.config.cors import setup_cors
from backend.core.config.help_func import check_platform
from backend.core.utils.logger_utils.exception_log_func import global_exception_handler, log_requests

from backend.api.backend_routers import api_router as backend_router
from frontend.routers import router as frontend_router

app = FastAPI()

app.include_router(backend_router)
app.include_router(frontend_router)

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="static")

setup_cors(app)

check_platform()

app.exception_handler(Exception)(global_exception_handler)
app.middleware("http")(log_requests)


@app.middleware("http")
async def fix_proxy_redirects(request: Request, call_next):
    response = await call_next(request)

    # Исправляем Location в заголовках, если прокси передал HTTP
    if response.status_code == 307 and "location" in response.headers:
        location = response.headers["location"]
        if location.startswith("http://"):
            response.headers["location"] = location.replace("http://", "https://")

    return response

