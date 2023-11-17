"""Test the OnNameChanged.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

# Houdini
import hou

# Tests


def test_OnNameChanged(mocker, execute_houdini_script):
    """Test the OnNameChanged.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("OnNameChanged", {"node": hou.node("/obj")})

    mock_emit.assert_called_with(
        HoudiniNodeEvent.OnNameChanged, {"node": hou.node("/obj")}
    )
