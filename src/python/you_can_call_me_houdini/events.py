"""This module contains custom event definitions."""
# pylint: disable=C0103

# You Can Call Me Houdini
from you_can_call_me_houdini.api.event import (
    Event,
    HoudiniEventEnum,
    HoudiniNodeEventEnum,
    RunOnceEvent,
)

# Classes


class HoudiniNodeEvent(HoudiniNodeEventEnum):
    """Enum related to node specific events."""

    OnCreated = Event("onnodecreate", description="Event when a node is created")
    OnDeleted = Event("ondeleted", description="Event when a node is deleted")
    OnInputChanged = Event(
        "onloaded", description="Event when a node's input is changed"
    )
    OnInstall = Event(
        "oninstall", description="Event when a node type is installed into the session"
    )
    OnLoaded = Event(
        "onloaded",
        description="Event after a node is created while loading a hip file (or pasted)",
    )
    OnNameChanged = Event(
        "onnamechanged", description="Event when a node's name is changed"
    )
    OnUninstall = Event(
        "onuninstall",
        description="Event when a node type is uninstalled from the session",
    )
    OnUpdated = Event(
        "onupdated", description="Event when an asset definition is updated"
    )
    PreFirstCreate = Event(
        "prefirstcreate",
        description="Event after the last instance of a node type is deleted",
    )
    PostLastDelete = Event(
        "postlastdelete",
        description="Event before the first instance of a node type is created",
    )


class HoudiniNodeGraphEvent(HoudiniEventEnum):
    """Enum related to node graph specific events."""

    PostKeyboardEvent = Event("postkeyboardevent")
    PostPasteEvent = Event(
        "postpasteevent",
        description="This event is emitted after nodes are pasted in the Network editor",
    )


class RopRenderEvent(HoudiniNodeEventEnum):
    """Enum related to ROP render specific events."""

    PostRender = Event("postrender")
    PostFrame = Event("postframe")
    PostWrite = Event("postwrite")
    PreFrame = Event("preframe")
    PreRender = Event("prerender")


class HoudiniSessionEvent(HoudiniEventEnum):
    """Enum related to Houdini session specific events."""

    AfterSceneSave = Event("afterscenesave")
    BeforeSceneSave = Event("beforescenesave")
    ExternalDragDrop = Event("externaldragdrop")
    HoudiniClose = Event("houdiniclose")
    NewScene = Event("newscene")
    SceneLoaded = Event("sceneloaded")


class HoudiniStartupEvent(HoudiniEventEnum):
    """Enum related to Houdini startup specific events."""

    NoHipCore = Event("nohipcore")  # houdinicore.py, before NoHip
    NoHipFX = Event("nohipfx")  # 123.py, before NoHip
    NoHip = Event("nohip")  # 123.py / houdinicore.py
    Any = Event("anyhip")  # Any time 456 is run.
    HoudiniStarted = RunOnceEvent(
        "houdinistarted"
    )  # Runs only the first time 456.py is executed.
    Ready = Event("ready")


class HoudiniUIEvent(HoudiniEventEnum):
    """Enum related to Houdini UI specific events."""

    UIReady = Event("postuiopen")
