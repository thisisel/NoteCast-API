from typing import Any


class PodchaserException(Exception):
    """Exception raised for errors in podchaser."""

    def __init__(
        self,
        message="Error in podchaser api",
        error: Any = None,
    ):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"PODCHASER ERROR : {self.message} \n {self.error} : "
