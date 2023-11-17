"""Perform events when an asset definition is updated."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

CallbackManager().emit(HoudiniNodeEvent.OnUpdated, kwargs)  # type: ignore  # noqa: F821
