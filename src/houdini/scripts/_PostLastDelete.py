"""Perform events after the last instance of a node type is deleted."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

CallbackManager().emit(HoudiniNodeEvent.PostLastDelete, kwargs)  # type: ignore  # noqa: F821
