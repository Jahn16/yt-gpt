import pytest

from app.providers.youtube import YoutubeClient


@pytest.fixture
def yt_id():
    return "0q8h5i5qC3w"


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
