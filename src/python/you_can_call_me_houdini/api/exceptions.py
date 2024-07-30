"""Exceptions for you_can_call_me."""

# Standard Library
from typing import Any

# Exceptions


class InvalidEventTypeError(Exception):
    """Exception raised when an event type is not an instance of HoudiniEventEnum."""

    def __init__(self, event_type: Any) -> None:
        super().__init__(f"{event_type} is not an instance of `HoudiniEventEnum`")
