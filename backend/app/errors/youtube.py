class YoutubeError(Exception):
    """
    Base class for YouTube errors
    """


class InvalidYoutubeIDError(YoutubeError):
    """
    Raised when YouTube ID is invalid
    """


class TranscriptNotFoundError(YoutubeError):
    """
    Raised when YouTube transcript is not found
    """
