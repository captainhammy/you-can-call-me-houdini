"""Test the pythonrc.py script."""

# Standard Library
import importlib

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini import events
from you_can_call_me_houdini.rop_render import print_post_frame

pytestmark = pytest.mark.usefixtures("add_pythonxylibs")


# Tests


@pytest.mark.parametrize("disable_rop_progress", (False, True))
def test_pythonrc(monkeypatch, mocker, disable_rop_progress):
    """Test the pythonrc.py module."""
    mock_manager = mocker.patch("you_can_call_me_houdini.api.manager.CallbackManager")

    mock_init_logging = mocker.patch("you_can_call_me_houdini.api.logger.init_config")

    if disable_rop_progress:
        monkeypatch.setenv("YOU_CAN_CALL_ME_HOUDINI_DISABLE_ROP_EVENTS", "1")

    import pythonrc

    importlib.reload(pythonrc)

    mock_init_logging.assert_called()

    if not disable_rop_progress:
        mock_manager.return_value.add_callback.assert_any_call(
            events.RopRenderEvent.PostFrame, print_post_frame
        )
