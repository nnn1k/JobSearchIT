import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

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
#app.middleware("http")(log_requests)


@app.middleware("http")
async def force_https(request: Request, call_next):
    response = await call_next(request)

    # Проверяем заголовок от прокси (Render.com передаёт его)
    if request.headers.get('x-forwarded-proto') == 'http':
        url = str(request.url).replace('http://', 'https://', 1)
        from starlette.responses import RedirectResponse
        return RedirectResponse(url, status_code=301)

    return response