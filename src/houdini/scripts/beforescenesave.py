"""Perform tasks before a scene is saved."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniSessionEvent

CallbackManager().emit(HoudiniSessionEvent.BeforeSceneSave, kwargs)  # type: ignore  # noqa: F821
