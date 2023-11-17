"""Tests for the you_can_call_me_houdini.callbacks module."""

# You Can Call Me Houdini
from you_can_call_me_houdini import callbacks
from you_can_call_me_houdini.events import HoudiniSessionEvent

# Tests


def test_emit_houdini_close(mocker):
    """Test you_can_call_me_houdini.callbacks.emit_houdini_close()."""
    mock_emit = mocker.patch.object(callbacks.CallbackManager, "emit")

    callbacks.emit_houdini_close()

    mock_emit.assert_called_with(HoudiniSessionEvent.HoudiniClose)


def test_run_123_cmd(mocker):
    """Test you_can_call_me_houdini.callbacks.run_123_cmd()."""
    mock_find = mocker.patch("hou.findFile")
    mock_hscript = mocker.patch("hou.hscript")

    callbacks.run_123_cmd({})

    mock_find.assert_called_with("scripts/123.cmd")
    mock_hscript.assert_called_with(f"source {mock_find.return_value}")
