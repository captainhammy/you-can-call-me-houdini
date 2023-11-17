"""This module contains callback related functions."""

# Future
from __future__ import annotations

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniSessionEvent

# Houdini
import hou


def emit_houdini_close() -> None:
    """Emit HoudiniSessionEvent.HoudiniClose event."""
    manager = CallbackManager()
    manager.emit(HoudiniSessionEvent.HoudiniClose)


def run_123_cmd(event_args: dict) -> None:  # pylint: disable=W0613
    """Source and execute 123.cmd.

    Args:
        event_args: The event related data.
    """
    cmd_123 = hou.findFile("scripts/123.cmd")

    hou.hscript(f"source {cmd_123}")
