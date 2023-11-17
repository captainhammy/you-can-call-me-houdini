"""This module contains the base api implementations for events."""

# Standard Library
import logging
from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Callable, Optional

# You Can Call Me Houdini
from you_can_call_me_houdini.api.stats import EventStats

# Common logger to use for the enum related logging. This should be better handled
# via the enum class setup but relies on Python 3.11+'s __init_subclass__ method.
event_logger = logging.getLogger(__name__)

# Classes


class HoudiniEventEnum(Enum):
    """Subclass for Houdini event enums."""

    def log_message(
        self, function: Callable, callback_args: dict  # pylint: disable=W0613
    ) -> None:
        """Log a callback call for the function and args.

        Args:
            function: The callback function.
            callback_args: The callback args.
        """
        event_logger.debug("%s: %s", self, f"{function.__module__}.{function.__name__}")


class HoudiniNodeEventEnum(HoudiniEventEnum):
    """Subclass for events dealing with Houdini nodes.

    The event args must contain a 'node' key pointing to the hou.Node instance.
    """

    def log_message(self, function: Callable, callback_args: dict) -> None:
        """Log a callback call for the function and args.

        Args:
            function: The callback function.
            callback_args: The callback args.

        """
        event_logger.debug(
            "%s: %s '%s'",
            self,
            f"{function.__module__}.{function.__name__}()",
            callback_args["node"].path(),
        )


@dataclass
class Event:
    """The base event class."""

    name: str
    enabled: bool = True
    description: Optional[str] = None
    stats: EventStats = field(init=False)
    stats_post_report: InitVar[bool] = False

    def __post_init__(self, stats_post_report: bool) -> None:
        self.stats = EventStats(self.name, post_report=stats_post_report)

    def post_run_callback(self) -> None:
        """Perform actions after the event has run."""


class RunOnceEvent(Event):
    """`Event` subclass that will only be run a single time.

    After the first run the event will be set as disabled.
    """

    def post_run_callback(self) -> None:
        """Perform actions after the event has run.

        This sets the `enabled` flag to False so the event will not run again.
        """
        self.enabled = False
