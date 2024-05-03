class GPTError(Exception):
    """
    Raised when GPT API request fails
    """


class ContextLengthError(GPTError):
    """
    Raised when context length is too long
    """

    def __init__(self) -> None:
        super().__init__("Context length is too long")
