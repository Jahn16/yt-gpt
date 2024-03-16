from fastapi import APIRouter

router = APIRouter(prefix="/transcribe")


@router.get("/")
def transcribe(youtube_url: str) -> dict[str, str]:
    return {"youtube_url": youtube_url}
