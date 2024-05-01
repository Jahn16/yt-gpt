import abc
from typing import cast

from pytube import YouTube


class YoutubeFetcher(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_video_title(yt_url: str) -> str:
        raise NotImplementedError


class PytubeFetcher(YoutubeFetcher):
    @staticmethod
    def get_video_title(yt_url: str) -> str:
        yt = YouTube(yt_url)
        return cast(str, yt.title)
