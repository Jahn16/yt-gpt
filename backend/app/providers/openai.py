import structlog
import tiktoken
from openai import APIError, AsyncOpenAI

from app.config import Settings
from app.errors.gpt import ContextLengthError, GPTError
from app.schemas.prompt import Prompt

logger = structlog.get_logger()


class OpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.openai_api_key

    def _calculate_tokens(self, prompt: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(prompt))
        return num_tokens

    def _select_model(self, message: str) -> str:
        num_tokens = self._calculate_tokens(message)
        logger.debug(num_tokens)
        if num_tokens > 16000:
            return "gpt-4-turbo"
        return "gpt-3.5-turbo"

    async def chat(self, prompt: Prompt) -> str:
        client = AsyncOpenAI(
            api_key=self._api_key,
        )

        message = f"You are an assistant that will receive a transcript from a video. Your task is to read the text and answer this question according to the text provided: {prompt.prompt}. Answer in the languague that the question is written in. The video title is {prompt.video.title} and trascript is: {prompt.video.transcription}. Respond using markdown format."  # noqa: E501
        model = self._select_model(message)
        await logger.ainfo("Chat completion started", model=model)
        try:
            chat_completion = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": message},
                ],
                model=model,
            )
        except APIError as e:
            await logger.aexception("Chat completion failed", model=model)
            if e.code == "context_length_exceeded":
                raise ContextLengthError()
            raise GPTError(e.message)
        await logger.ainfo("Chat completion completed", model=model)
        return chat_completion.choices[0].message.content or ""
