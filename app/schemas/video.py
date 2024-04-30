from pydantic import BaseModel


class Transcription(BaseModel):
    video_title: str
    transcription: str
