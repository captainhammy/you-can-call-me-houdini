"""Custom network editor event handlers."""

# Future
from __future__ import annotations

# Standard Library
from typing import List, Tuple

# You Can Call Me Houdini
from you_can_call_me_houdini.api import constants
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeGraphEvent

# Houdini
import hou
import nodegraphdisplay
import nodegraphutils
from canvaseventtypes import KeyboardEvent

# GLOBALS

_EVENT_TYPES = ("keyhit", "menukeyhit", "parentkeyhit")


# Non-Public Functions


def _execute_keyboard_callbacks(
    uievent: KeyboardEvent, pending_actions: List
) -> Tuple[None, bool]:
    scriptargs = {
        "pending_actions": pending_actions,
        "uievent": uievent,
        constants.CALLBACK_EVENT_TYPE: HoudiniNodeGraphEvent.PostKeyboardEvent,
    }

    for callback in CallbackManager().get_callbacks_for_event(
        HoudiniNodeGraphEvent.PostKeyboardEvent
    ):
        callback(scriptargs)

        if scriptargs.get(constants.KEYBOARD_EVENT_HANDLED, False):
            return None, True

    return None, False


def _handle_paste_event(uievent: KeyboardEvent) -> None:
    """Handle pasting and callback emission.

    Args:
        uievent: The occurring event.

    Returns:
        Return that the event handling was successful.
    """
    editor = uievent.editor
    eventtype = uievent.eventtype

    with hou.undos.group("Paste from clipboard"):
        nodegraphutils.pasteItems(editor)

        if eventtype != "parentkeyhit":
            if eventtype == "menukeyhit":
                mousepos = editor.screenBounds().center()

            else:
                mousepos = uievent.mousepos

            pos = editor.posFromScreen(mousepos)

            nodegraphutils.moveItemsToLocation(editor, pos, mousepos)

        nodegraphutils.updateCurrentItem(editor)

        scriptargs = {
            constants.PASTED_ITEMS: editor.pwd().selectedItems(),
            "uievent": uievent,
        }

        CallbackManager().emit(HoudiniNodeGraphEvent.PostPasteEvent, scriptargs)


def _is_paste_event(uievent: KeyboardEvent) -> bool:
    """Check whether the event is a h.paste event.

    Args:
        uievent: The occurring event.

    Returns:
        Whether the event is a paste event.
    """
    # Handle API changes in Houdini 20+.
    if hou.applicationVersion() > (20,):
        return nodegraphdisplay.setKeyPrompt(uievent.editor, uievent, "h.paste")

    return nodegraphdisplay.setKeyPrompt(
        uievent.editor, uievent.key, "h.paste", uievent.eventtype
    )


# Functions


def createEventHandler(  # pylint: disable=invalid-name
    uievent: KeyboardEvent, pending_actions: List
) -> Tuple[None, bool]:
    """Create an event handler for Houdini's network editor.

    Args:
        uievent: The occurring event.
        pending_actions: Pending actions.

    Returns:
        Handler event information.
    """

    if isinstance(uievent, KeyboardEvent) and uievent.eventtype in _EVENT_TYPES:
        if _is_paste_event(uievent):
            _handle_paste_event(uievent)

            return None, True

        return _execute_keyboard_callbacks(uievent, pending_actions)

    return None, False
