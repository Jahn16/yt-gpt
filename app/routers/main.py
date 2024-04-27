from fastapi import APIRouter, Depends

from app.config import Settings
from app.deps import get_settings
from app.providers.openai import OpenAIClient
from app.providers.youtube import YoutubeClient
from app.schemas.prompt import Prompt

router = APIRouter()


@router.get("/transcribe")
async def transcribe(youtube_url: str) -> str:
    transcription = YoutubeClient.get_transcript(youtube_url)
    return transcription


@router.post("/gpt")
async def gpt(
    prompt: Prompt, settings: Settings = Depends(get_settings)
) -> str:
    openai_client = OpenAIClient(settings)
    result = await openai_client.chat(prompt.prompt, prompt.transcription)

    return result
