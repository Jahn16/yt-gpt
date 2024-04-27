from pydantic import BaseModel


class Prompt(BaseModel):
    transcription: str
    prompt: str
