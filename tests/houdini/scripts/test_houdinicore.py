"""Test the houdinicore.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniStartupEvent

# Tests


def test_houdinicore(mocker, execute_houdini_script):
    """Test the houdinicore.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("houdinicore", None)

    mock_emit.assert_called_with(HoudiniStartupEvent.NoHip)
