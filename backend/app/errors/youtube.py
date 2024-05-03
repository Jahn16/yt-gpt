class YoutubeError(Exception):
    """
    Base class for YouTube errors
    """


class InvalidUrlError(YoutubeError):
    """
    Raised when YouTube URL is invalid
    """


class TranscriptNotFoundError(YoutubeError):
    """
    Raised when YouTube transcript is not found
    """
