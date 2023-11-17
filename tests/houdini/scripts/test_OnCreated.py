"""Test the OnCreated.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

# Houdini
import hou

# Tests


def test_OnCreated(mocker, execute_houdini_script):
    """Test the OnCreated.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("OnCreated", {"node": hou.node("/obj")})

    mock_emit.assert_called_with(HoudiniNodeEvent.OnCreated, {"node": hou.node("/obj")})
