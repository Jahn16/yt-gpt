import pytest
from youtube_transcript_api import (NoTranscriptFound, Transcript,
                                    TranscriptList)

from app.providers.youtube import YoutubeClient


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
    id = YoutubeClient._get_youtube_id(yt_url)
    assert id == yt_id


def test_get_yt_id_from_share_url(yt_id: str):
    yt_url = f"https://youtu.be/{yt_id}"
    id = YoutubeClient._get_youtube_id(yt_url)
    assert id == yt_id


def test_get_yt_id_url_with_query(yt_id: str):
    yt_url = f"https://www.youtube.com/watch?v={yt_id}&t=10s"
    id = YoutubeClient._get_youtube_id(yt_url)
    assert id == yt_id


def test_get_yt_id_invalid_url():
    yt_url = "https://example.com/invalid"
    with pytest.raises(ValueError):
        YoutubeClient._get_youtube_id(yt_url)


def test_get_transcription(
    transcript: Transcript, transcript_text: str, mocker
):
    mock_yt = mocker.patch("app.providers.youtube.YouTubeTranscriptApi")
    mock_yt.get_transcription.return_value = transcript
    mock_yt.format_transcript.return_value = transcript_text
    result = YoutubeClient.get_transcription(transcript._url)
    assert result == transcript_text


def test_get_transcription_not_found(
    yt_url: str, transcript: Transcript, transcript_text: str, mocker
):
    mock_yt = mocker.patch("app.providers.youtube.YouTubeTranscriptApi")
    mock_yt.get_transcription.side_effect = NoTranscriptFound
    mock_yt.list_transcriptions.return_value = TranscriptList(
        transcript.video_id, transcript._url, {"en": Transcript}, {}
    )
    result = YoutubeClient.get_transcription(yt_url)
    assert result == transcript_text
