"""Perform events before the first instance of a node type is created."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

CallbackManager().emit(HoudiniNodeEvent.PreFirstCreate, kwargs)  # type: ignore  # noqa: F821
