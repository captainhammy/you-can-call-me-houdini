"""Test the 123.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniStartupEvent

# Tests


def test_123(mocker, execute_houdini_script):
    """Test the 123.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("123", None)

    mock_emit.assert_called_with(HoudiniStartupEvent.NoHip)
