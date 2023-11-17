"""Test the OnLoaded.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

# Houdini
import hou

# Tests


def test_OnLoaded(mocker, execute_houdini_script):
    """Test the OnLoaded.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("OnLoaded", {"node": hou.node("/obj")})

    mock_emit.assert_called_with(HoudiniNodeEvent.OnLoaded, {"node": hou.node("/obj")})
