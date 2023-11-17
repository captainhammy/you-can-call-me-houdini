"""This module contains the Callback class definition."""

# Future
from __future__ import annotations

# Standard Library
from dataclasses import dataclass
from typing import Any, Callable, Optional

# You Can Call Me Houdini
from you_can_call_me_houdini.api import constants


@dataclass
class Callback:
    """Class to represent a named callback object which an associated callable.

    The callable is executed by calling this object.

    Args:
        name: The callback name.
        callback_function: The callable item to execute.
        enabled: Whether the callback is enabled.
    """

    name: str
    callback_function: Callable
    enabled: bool = True

    def __call__(self, callback_args: dict) -> Optional[Any]:
        # Only execute the callback function if this callback is enabled.
        if self.enabled:
            callback_args[constants.CALLBACK_EVENT_TYPE].log_message(
                self.callback_function, callback_args
            )

            return self.callback_function(callback_args)

        return None
