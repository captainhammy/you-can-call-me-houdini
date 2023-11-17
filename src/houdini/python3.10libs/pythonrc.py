"""Initialize package on Houdini startup."""

# Standard Library
import atexit
import os

# You Can Call Me Houdini
import you_can_call_me_houdini.api.logger

# Initialize the logging config before anything else.
you_can_call_me_houdini.api.logger.init_config()

# You Can Call Me Houdini
from you_can_call_me_houdini import callbacks, events
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.rop_render import (
    attach_rop_render_event,
    attach_rop_render_to_all_nodes,
    print_post_frame,
    print_post_render,
    print_post_write,
)

CallbackManager().add_callback(events.HoudiniStartupEvent.NoHip, callbacks.run_123_cmd)

# We need to add ROP render events to any ROP nodes which are created.
CallbackManager().add_callback(
    events.HoudiniNodeEvent.OnCreated, attach_rop_render_event
)

# We need to add ROP render events to any ROP nodes when a hip file is loaded.
CallbackManager().add_callback(
    events.HoudiniSessionEvent.SceneLoaded, attach_rop_render_to_all_nodes
)

if not os.getenv("YOU_CAN_CALL_ME_HOUDINI_DISABLE_ROP_EVENTS"):
    CallbackManager().add_callback(events.RopRenderEvent.PostFrame, print_post_frame)
    CallbackManager().add_callback(events.RopRenderEvent.PostWrite, print_post_write)
    CallbackManager().add_callback(events.RopRenderEvent.PostRender, print_post_render)

atexit.register(callbacks.emit_houdini_close)
