"""Perform events when a node type is installed into the session."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

CallbackManager().emit(HoudiniNodeEvent.OnInstall, kwargs)  # type: ignore  # noqa: F821
