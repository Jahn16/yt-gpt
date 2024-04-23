from fastapi import APIRouter, Depends

from app.config import Settings
from app.deps import get_settings
from app.providers.openai import OpenAIClient
from app.providers.youtube import YoutubeClient

router = APIRouter(prefix="/transcribe")


@router.get("/")
async def transcribe(
    youtube_url: str, prompt: str, settings: Settings = Depends(get_settings)
) -> str:
    transcription = YoutubeClient.get_transcript(youtube_url)
    openai_client = OpenAIClient(settings)
    result = await openai_client.chat(prompt, transcription)

    return result
