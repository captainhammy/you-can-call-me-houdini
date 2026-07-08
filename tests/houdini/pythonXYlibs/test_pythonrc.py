"""Test the pythonrc.py script."""

# Future
from __future__ import annotations

# Standard Library
import importlib
from typing import TYPE_CHECKING

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini import events
from you_can_call_me_houdini.rop_render import print_post_frame

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

pytestmark = pytest.mark.usefixtures("add_scripts_python")


# Tests


@pytest.mark.parametrize("disable_rop_progress", [False, True])
def test_pythonrc(monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture, disable_rop_progress: bool) -> None:
    """Test the pythonrc.py module."""
    mock_manager = mocker.patch("you_can_call_me_houdini.api.manager.CallbackManager")

    mock_init_logging = mocker.patch("you_can_call_me_houdini.api.logger.init_config")

    if disable_rop_progress:
        monkeypatch.setenv("YOU_CAN_CALL_ME_HOUDINI_DISABLE_ROP_EVENTS", "1")

    import pythonrc

    importlib.reload(pythonrc)

    mock_init_logging.assert_called()

    if not disable_rop_progress:
        mock_manager.return_value.add_callback.assert_any_call(events.RopRenderEvent.PostFrame, print_post_frame)
