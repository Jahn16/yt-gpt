from pydantic import BaseModel

from app.schemas.video import Video


class Prompt(BaseModel):
    video: Video
    prompt: str
