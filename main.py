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
#app.middleware("http")(log_requests)


@app.middleware("http")
async def force_https_urls(request: Request, call_next):
    response = await call_next(request)

    if isinstance(response, JSONResponse):
        import json
        data = json.loads(response.body.decode())

        # Рекурсивно заменяем http:// на https:// во всём JSON
        def fix_urls(obj):
            if isinstance(obj, str):
                return obj.replace("http://", "https://")
            elif isinstance(obj, dict):
                return {k: fix_urls(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [fix_urls(item) for item in obj]
            return obj

        fixed_data = fix_urls(data)
        response.body = json.dumps(fixed_data).encode()

    return response