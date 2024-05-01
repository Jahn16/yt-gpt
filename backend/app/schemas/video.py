from pydantic import BaseModel


class Video(BaseModel):
    title: str
    transcription: str
