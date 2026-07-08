"""Exceptions for you_can_call_me."""

# Exceptions


class InvalidEventTypeError(Exception):
    """Exception raised when an event type is not an instance of HoudiniEventEnum."""

    def __init__(self, event_type: object) -> None:
        super().__init__(f"{event_type} is not an instance of `HoudiniEventEnum`")
