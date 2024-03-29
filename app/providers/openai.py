from openai import AsyncOpenAI

from app.config import Settings


class OpenAIClient:
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.openai_api_key
        self._model = settings.openai_model

    async def chat(self, prompt: str, transcription: str) -> str:
        client = AsyncOpenAI(
            api_key=self._api_key,
        )

        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are an assistant that will receive a transcript from a video. Your task is to read the text and answer this question: {prompt}. Answer in the languague that the question is written in. The trascript is: {transcription}",  # noqa: E501
                },
            ],
            model=self._model,
        )
        return chat_completion.choices[0].message.content or ""
