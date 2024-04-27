from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.deps import get_settings
from app.routers import main
from app.utils.logger import setup_logging

setup_logging()

app = FastAPI(title="YT-GPT", version="0.1.0")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(main.router)

app.include_router(api_router)
