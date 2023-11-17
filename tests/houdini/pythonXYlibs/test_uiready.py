"""Test the uiready.py script."""

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniUIEvent

pytestmark = pytest.mark.usefixtures("add_pythonxylibs")


# Tests


def test_uiready(mocker):
    """Test the uiready.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    import uiready  # noqa: F401

    mock_emit.assert_called_with(HoudiniUIEvent.UIReady)
