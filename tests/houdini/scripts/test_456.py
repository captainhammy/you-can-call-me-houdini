"""Test the 456.py script."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniSessionEvent, HoudiniStartupEvent

# Tests


class Test_456:
    """Test the 456.py script."""

    def test_new_scene(self, mocker, execute_houdini_script):
        """Test when 456.py is run for a new scene."""
        mocker.patch("hou.hipFile.name", return_value="untitled.hip")

        mock_emit = mocker.patch.object(CallbackManager, "emit")

        execute_houdini_script("456", None)

        calls = [
            mocker.call(HoudiniStartupEvent.HoudiniStarted),
            mocker.call(HoudiniSessionEvent.NewScene),
            mocker.call(HoudiniStartupEvent.Any),
        ]

        mock_emit.assert_has_calls(calls)

    def test_opening_scene(self, mocker, execute_houdini_script):
        """Test when 456.py is run while loading a scene."""
        mocker.patch("hou.hipFile.name", return_value="test.hip")

        mock_emit = mocker.patch.object(CallbackManager, "emit")

        execute_houdini_script("456", None)

        calls = [
            mocker.call(HoudiniStartupEvent.HoudiniStarted),
            mocker.call(HoudiniSessionEvent.SceneLoaded),
            mocker.call(HoudiniStartupEvent.Any),
        ]

        mock_emit.assert_has_calls(calls)
