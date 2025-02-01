from fastapi import APIRouter, Depends, HTTPException
from structlog.contextvars import (
    bind_contextvars,
    unbind_contextvars
)

from app.config import Settings
from app.deps import get_settings
from app.errors.gpt import ContextLengthError, GPTError
from app.errors.youtube import InvalidYoutubeIDError, TranscriptNotFoundError
from app.providers.openai import OpenAIClient
from app.providers.youtube import YoutubeClient
from app.schemas.prompt import Prompt
from app.schemas.video import Video


router = APIRouter()


@router.get("/transcribe")
def transcribe(youtube_id: str) -> Video:
    bind_contextvars(yt_id=youtube_id)
    youtube_client = YoutubeClient()
    try:
        video_title = youtube_client.get_title(youtube_id)
        transcription = youtube_client.get_transcript(youtube_id)
    except InvalidYoutubeIDError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TranscriptNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    video = Video(title=video_title, transcription=transcription)
    unbind_contextvars("yt_id")
    return video


@router.post("/gpt")
async def gpt(
    prompt: Prompt, settings: Settings = Depends(get_settings)
) -> str:
    openai_client = OpenAIClient(settings)
    try:
        result = await openai_client.chat(prompt)
    except ContextLengthError:
        raise HTTPException(
            status_code=400,
            detail=(
                "The transcription is too long and cannot be processed. "
                "Please refresh and try a shorter video!"
            ),
        )
    except GPTError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result
