from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    cors_origins: list[str] = []
    openai_api_key: str
