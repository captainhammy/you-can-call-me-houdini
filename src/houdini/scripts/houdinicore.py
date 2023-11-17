"""Run events when Houdini Core is started without a scene (.hip) file."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniStartupEvent

CallbackManager().emit(HoudiniStartupEvent.NoHipCore)
CallbackManager().emit(HoudiniStartupEvent.NoHip)
