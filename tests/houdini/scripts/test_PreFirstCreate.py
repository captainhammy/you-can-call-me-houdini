"""Test the PreFirstCreate.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

# Houdini
import hou

# Tests


def test_PreFirstCreate(mocker, execute_houdini_script):
    """Test the PreFirstCreate.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("PreFirstCreate", {"node": hou.node("/obj")})

    mock_emit.assert_called_with(
        HoudiniNodeEvent.PreFirstCreate, {"node": hou.node("/obj")}
    )
