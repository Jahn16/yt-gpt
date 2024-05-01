from fastapi import APIRouter, Depends

from app.config import Settings
from app.deps import get_settings
from app.providers.openai import OpenAIClient
from app.providers.youtube import YoutubeClient
from app.schemas.prompt import Prompt
from app.schemas.video import Video

router = APIRouter()


@router.get("/transcribe")
async def transcribe(youtube_url: str) -> Video:
    youtube_client = YoutubeClient()
    video_title = youtube_client.get_title(youtube_url)
    transcription = youtube_client.get_transcript(youtube_url)
    return Video(title=video_title, transcription=transcription)


@router.post("/gpt")
async def gpt(
    prompt: Prompt, settings: Settings = Depends(get_settings)
) -> str:
    openai_client = OpenAIClient(settings)
    result = await openai_client.chat(prompt)

    return result
