import structlog
from openai import APIError, AsyncOpenAI

from app.config import Settings
from app.errors.gpt import ContextLengthError, GPTError
from app.schemas.prompt import Prompt

logger = structlog.get_logger()


class OpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.openai_api_key
        self._model = settings.openai_model

    async def chat(self, prompt: Prompt) -> str:
        client = AsyncOpenAI(
            api_key=self._api_key,
        )

        await logger.ainfo("Chat completion started")
        try:
            chat_completion = await client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an assistant that will receive a transcript from a video. Your task is to read the text and answer this question: {prompt.prompt}. Answer in the languague that the question is written in. The video title is {prompt.video.title} and trascript is: {prompt.video.transcription}. Respond using markdown format.",  # noqa: E501
                    },
                ],
                model=self._model,
            )
        except APIError as e:
            await logger.aexception("Chat completion failed")
            if e.code == "context_length_exceeded":
                raise ContextLengthError()
            raise GPTError(e.message)
        await logger.ainfo("Chat completion completed")
        return chat_completion.choices[0].message.content or ""
