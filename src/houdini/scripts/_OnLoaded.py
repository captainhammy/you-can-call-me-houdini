"""Perform events after a node is created while loading a hip file (or pasted)."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

CallbackManager().emit(HoudiniNodeEvent.OnLoaded, kwargs)  # type: ignore  # noqa: F821
