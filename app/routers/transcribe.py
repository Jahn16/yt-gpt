from fastapi import APIRouter

from app.providers.youtube import YoutubeClient

router = APIRouter(prefix="/transcribe")


@router.get("/")
def transcribe(youtube_url: str) -> str:
    transcription = YoutubeClient.get_transcript(youtube_url)
    return transcription
