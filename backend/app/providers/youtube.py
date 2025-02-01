import abc
from typing import cast

import structlog
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from youtube_transcript_api import (
    NoTranscriptFound,
    Transcript,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.formatters import TextFormatter

from app.errors.youtube import InvalidYoutubeIDError, TranscriptNotFoundError

logger = structlog.get_logger()


class YoutubeClient:
    def __init__(self) -> None:
        self._metadata_fetcher = PytubeFetcher
        self._transcript_fetcher = TranscriptFetcher

    def get_title(self, yt_url: str) -> str:
        logger.info("Fetching youtube title", yt_id=yt_url)
        return self._metadata_fetcher.get_video_title(yt_url)

    def get_transcript(self, yt_url: str) -> str:
        logger.info("Fetching youtube transcript", yt_id=yt_url)
        return self._transcript_fetcher.get_transcript(yt_url)


class MetadataFetcher(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_video_title(yt_id: str) -> str:
        raise NotImplementedError


class PytubeFetcher(MetadataFetcher):
    @staticmethod
    def get_video_title(yt_id: str) -> str:
        yt_url = f"https://www.youtube.com/watch?v={yt_id}"
        try:
            yt = YouTube(yt_url)
            title = yt.title
        except (RegexMatchError, VideoUnavailable):
            logger.warning("Invalid YouTube URL", youtube_url=yt_id)
            raise InvalidYoutubeIDError(f"Invalid YouTube ID: {yt_id}")
        return cast(str, title)


class TranscriptFetcher:
    @staticmethod
    def get_transcript(yt_id: str) -> str:
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
