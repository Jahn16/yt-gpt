import abc
from typing import cast

import structlog
from youtube_transcript_api import (
    NoTranscriptFound,
    Transcript,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.formatters import TextFormatter

from app.errors.youtube import InvalidYoutubeIDError, TranscriptNotFoundError
import requests
from bs4 import BeautifulSoup

logger = structlog.get_logger()


class YoutubeClient:
    def __init__(self) -> None:
        self._metadata_fetcher = RequestFetcher
        self._transcript_fetcher = TranscriptFetcher

    def get_title(self, yt_id: str) -> str:
        logger.info("Fetching youtube title", yt_id=yt_id)
        return self._metadata_fetcher.get_video_title(yt_id)

    def get_transcript(self, yt_id: str) -> str:
        logger.info("Fetching youtube transcript", yt_id=yt_id)
        return self._transcript_fetcher.get_transcript(yt_id)


class MetadataFetcher(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_video_title(yt_id: str) -> str:
        raise NotImplementedError


class RequestFetcher(MetadataFetcher):
    @staticmethod
    def get_video_title(yt_id: str) -> str:
        yt_url = f"https://www.youtube.com/watch?v={yt_id}"
        res = requests.get(yt_url)
        soup = BeautifulSoup(res.text, "html.parser")
        titles = soup.find_all(name="title")
        if not titles:
            logger.warning("No title found")
            return ""
        return titles[0].text.replace(" - YouTube", "")


class TranscriptFetcher:
    @staticmethod
    def get_transcript(yt_id: str) -> str:
        formatter = TextFormatter()
        try:
            transcript_lines: list[
                dict[str, str]
            ] = YouTubeTranscriptApi.get_transcript(yt_id)
        except TranscriptsDisabled:
            logger.warning("Transcripts disabled")
            raise TranscriptNotFoundError(
                "Transcripts disabled for this video"
            )
        except NoTranscriptFound:
            logger.info("No english transcript found")
        else:
            logger.info("Transcript found")
            return cast(str, formatter.format_transcript(transcript_lines))

        transcript_list = YouTubeTranscriptApi.list_transcripts(yt_id)
        try:
            transcript: Transcript = transcript_list.__iter__().__next__()
        except StopIteration:
            logger.info("No transcript found")
            raise TranscriptNotFoundError("No transcript found")
        transcript_lines = transcript.fetch()
        logger.info(
            "Transcript found",
            youtube_id=yt_id,
            language=transcript.language_code,
        )
        return cast(str, formatter.format_transcript(transcript_lines))
