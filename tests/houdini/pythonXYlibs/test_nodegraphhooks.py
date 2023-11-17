"""Test the nodegraphhooks.py module.

Notes on module testing/mocking:

Because the nodegraph stuff is so heavily hou.ui dependent we  have to
explicitly import it inside the test functions so that the imports occur
after all the necessary module mocking that would cause hou.ui issues. We
then must reload the module in order for the already loaded version to
pick up the active monkeypatched modules so that our testing is accurate.

"""

# Future
from __future__ import annotations

# Standard Library
import importlib
import sys

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini import events
from you_can_call_me_houdini.api import constants, manager

# Houdini
import hou

# Ensure we're getting things from our location and not $HFS.
pytestmark = pytest.mark.usefixtures("add_pythonxylibs")


# Fixtures


@pytest.fixture
def mock_nodegraphutils(monkeypatch, mocker):
    """Mock nodegraphutils which can't be imported when running tests via Hython."""
    mocked_nodegraphutils = mocker.MagicMock()

    monkeypatch.setitem(sys.modules, "nodegraphutils", mocked_nodegraphutils)

    yield mocked_nodegraphutils


@pytest.fixture
def mock_nodegraphdisplay(monkeypatch, mocker):
    """Mock nodegraphdisplay which can't be imported when running tests via Hython."""
    mocked_nodegraphdisplay = mocker.MagicMock()

    monkeypatch.setitem(sys.modules, "nodegraphdisplay", mocked_nodegraphdisplay)

    yield mocked_nodegraphdisplay


# Tests


@pytest.mark.parametrize("callback_handled", (False, True))
def test__execute_keyboard_callbacks(
    mocker, mock_nodegraphutils, mock_nodegraphdisplay, callback_handled
):
    """Test nodegraphhooks._execute_keyboard_callbacks()."""
    import nodegraphhooks

    importlib.reload(
        nodegraphhooks
    )  # Reload to module mocking works across parametrization

    mock_event = mocker.MagicMock(spec=nodegraphhooks.KeyboardEvent)
    mock_pending = mocker.MagicMock(spec=list)

    def test_callback(scriptargs):
        if callback_handled:
            scriptargs[constants.KEYBOARD_EVENT_HANDLED] = True

    callbacks = [
        mocker.MagicMock(),
        test_callback,
    ]

    mocker.patch.object(
        manager.CallbackManager, "get_callbacks_for_event", return_value=callbacks
    )

    result = nodegraphhooks._execute_keyboard_callbacks(mock_event, mock_pending)

    assert result == (None, callback_handled)


@pytest.mark.parametrize(
    "event_type, mousepos",
    (
        ("menukeyhit", hou.Vector2(1, 2)),
        ("keyhit", hou.Vector2(3, 4)),
        ("parentkeyhit", None),
    ),
)
def test__handle_paste_event(
    mocker, mock_nodegraphutils, mock_nodegraphdisplay, event_type, mousepos
):
    """Test nodegraphhooks._handle_paste_event()."""
    mock_emit = mocker.patch.object(manager.CallbackManager, "emit")

    mock_items = mocker.MagicMock(spec=tuple)

    import nodegraphhooks

    importlib.reload(
        nodegraphhooks
    )  # Reload to module mocking works across parametrization

    mock_editor = mocker.MagicMock()
    mock_editor.pwd.return_value.selectedItems.return_value = mock_items

    mock_event = mocker.MagicMock()
    mock_event.editor = mock_editor
    mock_event.eventtype = event_type

    if event_type == "menukeyhit":
        mock_editor.screenBounds.return_value.center.return_value = mousepos

    elif event_type != "parentkeyhit":
        mock_event.mousepos = mousepos

    nodegraphhooks._handle_paste_event(mock_event)

    if event_type != "parentkeyhit":
        mock_editor.posFromScreen.assert_called_with(mousepos)
        mock_nodegraphutils.moveItemsToLocation.assert_called()

    expected_args = {
        constants.PASTED_ITEMS: mock_items,
        "uievent": mock_event,
    }
    mock_emit.assert_called_with(
        events.HoudiniNodeGraphEvent.PostPasteEvent, expected_args
    )


@pytest.mark.parametrize("houdini_version", ((20, 0, 123), (19, 5, 456)))
def test__is_paste_event(
    mocker, mock_nodegraphutils, mock_nodegraphdisplay, houdini_version
):
    """Test nodegraphhooks._is_paste_event()."""
    import nodegraphhooks

    importlib.reload(
        nodegraphhooks
    )  # Reload to module mocking works across parametrization

    mocker.patch("hou.applicationVersion", return_value=houdini_version)

    mock_event = mocker.MagicMock()
    result = nodegraphhooks._is_paste_event(mock_event)

    assert result == mock_nodegraphdisplay.setKeyPrompt.return_value


@pytest.mark.parametrize(
    "is_keyboard_event, is_known_type, is_paste_event, expected",
    (
        (False, False, False, False),
        (True, False, False, False),
        (True, True, False, True),
        (True, True, True, True),
    ),
)
def test_createEventHandler(
    mocker,
    mock_nodegraphutils,
    mock_nodegraphdisplay,
    is_keyboard_event,
    is_known_type,
    is_paste_event,
    expected,
):
    """Test nodegraphhooks.createEventHandler()."""
    import nodegraphhooks

    importlib.reload(
        nodegraphhooks
    )  # Reload to module mocking works across parametrization

    mocker.patch("nodegraphhooks._is_paste_event", return_value=is_paste_event)
    mock_handle_paste = mocker.patch("nodegraphhooks._handle_paste_event")

    mock_execute = mocker.patch(
        "nodegraphhooks._execute_keyboard_callbacks", return_value=(None, True)
    )

    if is_keyboard_event:
        event = mocker.MagicMock(spec=nodegraphhooks.KeyboardEvent)

    else:
        event = mocker.MagicMock()

    event.eventtype = "menukeyhit" if is_known_type else "other"

    mock_pending = mocker.MagicMock(spec=list)

    result = nodegraphhooks.createEventHandler(event, mock_pending)

    assert result == (None, expected)

    if is_paste_event:
        mock_handle_paste.assert_called()

    elif is_known_type:
        mock_execute.assert_called()
