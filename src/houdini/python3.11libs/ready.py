"""Perform tasks after Houdini's non-graphical components are ready."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniStartupEvent

CallbackManager().emit(HoudiniStartupEvent.Ready)
