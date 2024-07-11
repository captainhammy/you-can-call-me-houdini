"""Perform tasks after Houdini's UI is ready."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniUIEvent

CallbackManager().emit(HoudiniUIEvent.UIReady)
