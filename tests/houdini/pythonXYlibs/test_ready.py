"""Test the ready.py script."""

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniStartupEvent

# Houdini
import hou

pytestmark = pytest.mark.usefixtures("add_pythonxylibs")


# Tests


@pytest.mark.skipif(hou.applicationVersion() < (20,), reason="File added in Houdini 20.0")
def test_ready(mocker):
    """Test the ready.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    import ready  # noqa: F401

    mock_emit.assert_called_with(HoudiniStartupEvent.Ready)
