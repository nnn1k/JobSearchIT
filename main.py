from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import router as backend_router
from frontend.routers import router as frontend_router

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="static")
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
