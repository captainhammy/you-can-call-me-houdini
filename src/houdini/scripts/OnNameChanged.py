"""Perform events when a node's name is changed."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

CallbackManager().emit(HoudiniNodeEvent.OnNameChanged, kwargs)  # type: ignore  # noqa: F821
