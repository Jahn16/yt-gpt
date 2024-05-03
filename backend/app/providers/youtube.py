import abc
from typing import cast
from urllib.parse import parse_qs, urlparse

import structlog
from pytube import YouTube
from youtube_transcript_api import (
    NoTranscriptFound,
    Transcript,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.formatters import TextFormatter

from app.errors.youtube import InvalidUrlError, TranscriptNotFoundError

logger = structlog.get_logger()


class YoutubeClient:
    def __init__(self) -> None:
        self._metadata_fetcher = PytubeFetcher
        self._transcript_fetcher = TranscriptFetcher

    def get_title(self, yt_url: str) -> str:
        return self._metadata_fetcher.get_video_title(yt_url)

    def get_transcript(self, yt_url: str) -> str:
        return self._transcript_fetcher.get_transcript(yt_url)


class MetadataFetcher(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_video_title(yt_url: str) -> str:
        raise NotImplementedError


class PytubeFetcher(MetadataFetcher):
    @staticmethod
    def get_video_title(yt_url: str) -> str:
        yt = YouTube(yt_url)
        return cast(str, yt.title)


class TranscriptFetcher:
    @staticmethod
    def _get_youtube_id(yt_url: str) -> str:
        parse_result = urlparse(yt_url)
        if parse_result.netloc == "www.youtube.com":
            query = parse_qs(parse_result.query)
            if "v" in query:
                return query["v"][0]
        elif parse_result.netloc == "youtu.be":
            return parse_result.path[1:]
        raise InvalidUrlError(f"Invalid YouTube URL: {yt_url}")

    @staticmethod
    def get_transcript(yt_url: str) -> str:
        yt_id = TranscriptFetcher._get_youtube_id(yt_url)

        logger.info("Fetching transcript", youtube_id=yt_id)
        formatter = TextFormatter()
        try:
            transcript_lines: list[
                dict[str, str]
            ] = YouTubeTranscriptApi.get_transcript(yt_id)
        except TranscriptsDisabled:
            logger.warning("Transcripts disabled", youtube_id=yt_id)
            raise TranscriptNotFoundError(
                "Transcripts disabled for this video"
            )
        except NoTranscriptFound:
            logger.info("No english transcript found", youtube_id=yt_id)
        else:
            logger.info("Transcript found", youtube_id=yt_id)
            return cast(str, formatter.format_transcript(transcript_lines))

        transcript_list = YouTubeTranscriptApi.list_transcripts(yt_id)
        try:
            transcript: Transcript = transcript_list.__iter__().__next__()
        except StopIteration:
            logger.info("No transcript found", youtube_id=yt_id)
            raise TranscriptNotFoundError("No transcript found")
        transcript_lines = transcript.fetch()
        logger.info(
            "Transcript found",
            youtube_id=yt_id,
            language=transcript.language_code,
        )
        return cast(str, formatter.format_transcript(transcript_lines))
