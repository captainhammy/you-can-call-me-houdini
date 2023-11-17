"""This module contains the implementation for the callback manager."""

# Future
from __future__ import annotations

# Standard Library
import logging
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Callable, Dict, Generator, List, Optional

# You Can Call Me Houdini
from you_can_call_me_houdini.api import constants
from you_can_call_me_houdini.api.callback import Callback
from you_can_call_me_houdini.api.event import HoudiniEventEnum
from you_can_call_me_houdini.api.metaclasses import Singleton

# Houdini
import hou

# Classes

logger = logging.getLogger(__name__)


@dataclass
class CallbackManager(metaclass=Singleton):
    """The callback managing class.

    This class is a singleton.
    """

    callbacks: Dict[HoudiniEventEnum, List[Callback]] = field(default_factory=dict)

    def add_callback(
        self,
        event: HoudiniEventEnum,
        callback_function: Callable,
        name: Optional[str] = None,
        enabled: bool = True,
        skip_no_ui: bool = False,
    ) -> Optional[Callback]:
        """Add a callback against an event.

        If skipping in the event of the UI being unavailable and the UI is actually unavailable then
        the callback will skip being registered entirely, not merely disabled.

        Args:
            event: The event to register the callback for.
            callback_function: The callable to execute.
            name: An optional callback name.
            enabled: Whether the callback should be enabled by default.
            skip_no_ui: Whether to skip registration if the UI is not present.

        Returns:
            The created Callback object, if any.
        """
        if skip_no_ui and not hou.isUIAvailable():
            return None

        event_callbacks = self.callbacks.setdefault(event, [])

        name = name or callback_function.__name__

        callback = Callback(name, callback_function, enabled=enabled)

        event_callbacks.append(callback)

        return callback

    def emit(
        self, event_type: HoudiniEventEnum, callback_args: Optional[dict] = None
    ) -> None:
        """Emit an event and execute any assigned callbacks.

        Args:
            event_type: The event type being emitted.
            callback_args: Optional argument dictionary to pass to any callbacks.
        """
        if not isinstance(event_type, HoudiniEventEnum):
            raise TypeError(f"{event_type} is not an instance of {HoudiniEventEnum}")

        event = event_type.value

        # Skip disabled events.
        if not event.enabled:
            return

        callback_args = callback_args if callback_args is not None else {}

        # Temporarily add the event type to the callback args in case anything being
        # executed wants to know the context (such as logging including the event name.)
        callback_args[constants.CALLBACK_EVENT_TYPE] = event_type

        with event.stats:
            for callback in self.callbacks.get(event_type, ()):
                callback(callback_args)

        # Remove the temporarily added event type information.
        del callback_args[constants.CALLBACK_EVENT_TYPE]

        event.post_run_callback()

    def get_callbacks_for_event(self, event_type: HoudiniEventEnum) -> List[Callback]:
        """Get a list of callbacks for an event.

        If the event is disabled then an empty list will be returned.

        Args:
            event_type: The event type to get the callbacks for.

        Returns:
            A list of matching callbacks, if any.
        """
        if not event_type.value.enabled:
            return []

        return self.callbacks.get(event_type, [])

    @contextmanager
    def ignore_event_callbacks(
        self, events: Optional[HoudiniEventEnum | List[HoudiniEventEnum]] = None
    ) -> Generator[None, None, None]:
        """Disable events during the scope.

        >>> with CallbackManager.ignore_event_callbacks():
            # Perform actions which would normally trigger callbacks but will not
            # for the scope of the block.

        Args:
            events: Optional single event or list of events. If None, all events will be disabled.
        """
        # If no events are provided then we will disable all of them.
        if events is None:
            events = list(self.callbacks)

        elif isinstance(events, HoudiniEventEnum):
            events = [events]

        event_states = {}

        # Stash the current enabled state for each event being disabled and disable it.
        for event in events:
            event_states[event] = event.value.enabled
            event.value.enabled = False

        # Yield from within the 'try' such that if an exception occurs the 'finally' will
        # be engaged so that the enabled states are restored.
        try:
            yield

        finally:
            for event, state in event_states.items():
                event.value.enabled = state
