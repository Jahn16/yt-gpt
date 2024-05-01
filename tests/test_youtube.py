import pytest
from youtube_transcript_api import (
    NoTranscriptFound,
    Transcript,
    TranscriptList,
)

from app.providers.youtube import TranscriptFetcher


@pytest.fixture
def yt_id() -> str:
    return "0q8h5i5qC3w"


@pytest.fixture
def yt_url(yt_id: str) -> str:
    return f"https://www.youtube.com/watch?v={yt_id}"


@pytest.fixture
def transcript(yt_id: str, yt_url: str) -> Transcript:
    return Transcript(None, yt_id, yt_url, "English", "en", False, [])


@pytest.fixture
def transcript_text():
    return "transcript"


def test_get_yt_id_normal_url(yt_id: str):
    yt_url = f"https://www.youtube.com/watch?v={yt_id}"
    id = TranscriptFetcher._get_youtube_id(yt_url)
    assert id == yt_id


def test_get_yt_id_from_share_url(yt_id: str):
    yt_url = f"https://youtu.be/{yt_id}"
    id = TranscriptFetcher._get_youtube_id(yt_url)
    assert id == yt_id


def test_get_yt_id_url_with_query(yt_id: str):
    yt_url = f"https://www.youtube.com/watch?v={yt_id}&t=10s"
    id = TranscriptFetcher._get_youtube_id(yt_url)
    assert id == yt_id


def test_get_yt_id_invalid_url():
    yt_url = "https://example.com/invalid"
    with pytest.raises(ValueError):
        TranscriptFetcher._get_youtube_id(yt_url)


def test_get_transcript(transcript: Transcript, transcript_text: str, mocker):
    mock_yt = mocker.patch("app.providers.youtube.YouTubeTranscriptApi")
    mock_formatter = mocker.patch("app.providers.youtube.TextFormatter")
    mock_yt.get_transcript.return_value = transcript
    mock_formatter().format_transcript.return_value = transcript_text
    result = TranscriptFetcher.get_transcript(transcript._url)
    assert result == transcript_text


def test_get_transcript_not_found(
    yt_url: str, transcript: Transcript, transcript_text: str, mocker
):
    mock_yt = mocker.patch("app.providers.youtube.YouTubeTranscriptApi")
    mock_formatter = mocker.patch("app.providers.youtube.TextFormatter")
    mock_yt.get_transcript.side_effect = NoTranscriptFound(
        transcript.video_id, "en", None
    )
    mock_yt.list_transcripts.return_value = TranscriptList(
        transcript.video_id, {"en": Transcript}, {}, [{}]
    )
    mock_formatter().format_transcript.return_value = transcript_text
    result = TranscriptFetcher.get_transcript(yt_url)
    assert result == transcript_text
    mock_formatter().format_transcript.assert_called_with(transcript)
