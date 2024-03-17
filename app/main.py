from fastapi import APIRouter, FastAPI

from app.routers import transcribe
from app.utils.logger import setup_logging

setup_logging()

app = FastAPI(title="YT-GPT", version="0.1.0")


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(transcribe.router)

app.include_router(api_router)
