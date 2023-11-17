"""Test the beforescenesave.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniSessionEvent

# Houdini
import hou

# Tests


def test_beforescenesave(mocker, execute_houdini_script):
    """Test the beforescenesave.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("beforescenesave", {"node": hou.node("/obj")})

    mock_emit.assert_called_with(
        HoudiniSessionEvent.BeforeSceneSave, {"node": hou.node("/obj")}
    )
