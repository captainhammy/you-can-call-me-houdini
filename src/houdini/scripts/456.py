"""Run events when Houdini loads a scene file (including when Houdini starts up with a scene file)."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniSessionEvent, HoudiniStartupEvent

# Houdini
import hou

CallbackManager().emit(HoudiniStartupEvent.HoudiniStarted)

# Switch to `hou.hipFile.isNewFile()` when #129624 is fixed. Currently, it incorrectly returns
# True when opening a file.
# if hou.hipFile.isNewFile()
if hou.hipFile.name() == "untitled.hip":
    CallbackManager().emit(HoudiniSessionEvent.NewScene)

else:
    CallbackManager().emit(HoudiniSessionEvent.SceneLoaded)

CallbackManager().emit(HoudiniStartupEvent.Any)
