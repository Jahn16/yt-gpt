from urllib.parse import parse_qs, urlparse

import structlog
from youtube_transcript_api import (
    NoTranscriptFound,
    Transcript,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)
from youtube_transcript_api.formatters import TextFormatter

logger = structlog.get_logger()


class YoutubeClient:
    @staticmethod
    def _get_youtube_id(yt_url: str) -> str:
        parse_result = urlparse(yt_url)
        if parse_result.netloc == "www.youtube.com":
            query = parse_qs(parse_result.query)
            if "v" in query:
                return query["v"][0]
        elif parse_result.netloc == "youtu.be":
            return parse_result.path[1:]
        raise ValueError(f"Invalid YouTube URL: {yt_url}")

    @staticmethod
    def get_transcript(yt_url: str):
        yt_id = YoutubeClient._get_youtube_id(yt_url)

        logger.info("Fetching transcript", youtube_id=yt_id)
        formatter = TextFormatter()
        try:
            transcript_lines: list[
                dict[str, str]
            ] = YouTubeTranscriptApi.get_transcript(yt_id)
        except TranscriptsDisabled as e:
            logger.warning("Transcripts disabled", youtube_id=yt_id)
            raise e
        except NoTranscriptFound:
            logger.info("No english transcript found", youtube_id=yt_id)
        else:
            logger.info("Transcript found", youtube_id=yt_id)
            return formatter.format_transcript(transcript_lines)

        transcript_list = YouTubeTranscriptApi.list_transcripts(yt_id)
        transcript: Transcript = transcript_list.__iter__().__next__()
        transcript_lines = transcript.fetch()
        logger.info(
            "Transcript found",
            youtube_id=yt_id,
            language=transcript.language_code,
        )
        return formatter.format_transcript(transcript_lines)
