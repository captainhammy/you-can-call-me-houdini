"""Code to handle emitting and maintaining data between related ROP render events."""

# Future
from __future__ import annotations

# Standard Library
import pathlib
import re
import time
from dataclasses import dataclass
from typing import Dict, List

# Third Party
import humanfriendly

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.api.metaclasses import Singleton
from you_can_call_me_houdini.events import RopRenderEvent

# Houdini
import hou

# Globals

_FILE_PARM_MAP = {
    "Driver/alembic": "filename",
    "Driver/comp": "copoutput",
    "Driver/geometry": "sopoutput",
    "Driver/usd": "lopoutput",
    "Sop/rop_geometry": "sopoutput",
    "Sop/rop_alembic": "filename",
}


# Classes


@dataclass
class RopRenderProcess:
    """A class representing a ROP node in the process of rendering."""

    node: hou.RopNode
    output_parameter: hou.Parm = None
    has_post_write: bool = False
    render_count: int = 0
    render_start_time: float = 0
    frame_start_time: float = 0
    frame_padding: int = 1

    def __post_init__(self) -> None:
        output_parm_name = _FILE_PARM_MAP.get(self.node.type().nameWithCategory())

        if output_parm_name is not None:
            parm = self.node.parm(output_parm_name)

            if parm is not None:
                self.output_parameter = parm

        if self.node.parm("postwrite") is not None:
            self.has_post_write = True

    def pre_render(self, event_args: dict) -> None:
        """Emit a `RopRenderEvent.PreRender` with relevant data.

        Args:
            event_args: The event related data.
        """
        if self.output_parameter is not None:
            self.frame_padding = _get_frame_padding(self.output_parameter)

        self.render_count += 1
        self.render_start_time = time.time()

        args = {
            "process": self,
            "node": self.node,
            "scene_time": event_args["scene_time"],
            "render_count": self.render_count,
            "render_start_time": self.render_start_time,
        }

        CallbackManager().emit(RopRenderEvent.PreRender, args)

    def pre_frame(self, event_args: dict) -> None:
        """Emit a `RopRenderEvent.PreFrame` with relevant data.

        Args:
            event_args: The event related data.
        """
        self.frame_start_time = time.time()

        args = {
            "process": self,
            "node": self.node,
            "scene_time": event_args["scene_time"],
            "render_count": self.render_count,
            "render_start_time": self.render_start_time,
            "frame_start_time": self.frame_start_time,
            "frame_padding": self.frame_padding,
        }

        if self.output_parameter is not None:
            args["output_path"] = self.output_parameter.evalAtTime(
                event_args["scene_time"]
            )

        CallbackManager().emit(RopRenderEvent.PreFrame, args)

    def post_frame(self, event_args: dict) -> None:
        """Emit a `RopRenderEvent.PostFrame` with relevant data.

        Args:
            event_args: The event related data.
        """
        end_time = time.time()
        frame_time = end_time - self.frame_start_time

        args = {
            "process": self,
            "node": self.node,
            "scene_time": event_args["scene_time"],
            "render_count": self.render_count,
            "render_start_time": self.render_start_time,
            "frame_start_time": self.frame_start_time,
            "frame_end_time": end_time,
            "frame_time": frame_time,
            "frame_padding": self.frame_padding,
        }

        if self.output_parameter is not None:
            args["output_path"] = self.output_parameter.evalAtTime(
                event_args["scene_time"]
            )

        CallbackManager().emit(RopRenderEvent.PostFrame, args)

    def post_render(self, event_args: dict) -> None:
        """Emit a `RopRenderEvent.PostRender` with relevant data.

        Args:
            event_args: The event related data.
        """
        end_time = time.time()
        render_time = end_time - self.render_start_time

        args = {
            "process": self,
            "node": self.node,
            "scene_time": event_args["scene_time"],
            "render_count": self.render_count,
            "render_start_time": self.render_start_time,
            "render_end_time": end_time,
            "render_time": render_time,
        }

        CallbackManager().emit(RopRenderEvent.PostRender, args)

    def post_write(self, event_args: dict) -> None:
        """Emit a `RopRenderEvent.PostWrite` with relevant data.

        Args:
            event_args: The event related data.
        """
        args = {
            "process": self,
            "node": self.node,
            "scene_time": event_args["scene_time"],
        }

        if self.output_parameter is not None:
            args["output_path"] = self.output_parameter.evalAtTime(
                event_args["scene_time"]
            )

        CallbackManager().emit(RopRenderEvent.PostWrite, args)


class RopRenderFactory(metaclass=Singleton):
    """Singleton class to manage mappings between rendering ROP nodes and their process data."""

    _node_processes: Dict[hou.OpNode, RopRenderProcess] = {}

    def get_process_for_node(self, node: hou.RopNode) -> RopRenderProcess:
        """Find or create a `RopRenderProcess` for a ROP node.

        Args:
            node: The node to find or create a `RopRenderProcess` for.

        Returns:
            An existing or new `RopRenderProcess`.
        """
        process = self._node_processes.get(node)

        if process is None:
            process = RopRenderProcess(node)
            self._node_processes[node] = process

        return process


# Non-Public Functions


def _find_all_rop_instances() -> List[hou.RopNode]:
    """Find a list of all Houdini nodes in the scene which are ROP nodes.

    Returns:
        A list of ROP node instances.
    """
    rop_instances = []

    # Get all the candidate node type definitions we want to check.
    rop_types = _find_all_rop_types()

    for node_type in rop_types:
        instances = node_type.instances()

        if not instances:
            continue

        rop_instances.extend(instances)

    return rop_instances


def _find_all_rop_types() -> List[hou.OpNodeType]:
    """Find a list of all Houdini node types which are ROPs.

    Returns:
        A list of all the found ROP node types.
    """
    # Start with all the node types under the standard Driver/ROP context, removing the manager ones.
    rop_types = [
        node_type
        for node_type in hou.ropNodeTypeCategory().nodeTypes().values()
        if not node_type.isManager()
    ]

    # Finding ROP node types that exist in other contexts is more tricky. The best way to do this seems
    # to be to look for node types which ARE managers but do NOT allow for any children. SideFX has confirmed
    # that the fact the ROP node types are managers is expected and that this is a safe way to go about things.
    # We'll do extra confirmation elsewhere to ensure that instances are in fact hou.RopNodes, this just helps
    # to greatly narrow down the types we need to check.
    for category in hou.nodeTypeCategories().values():
        # Skip this as we've already done it above and the logic doesn't apply to actual ROP nodes.
        if category == hou.ropNodeTypeCategory():
            continue

        rop_types.extend(
            [
                node_type
                for node_type in category.nodeTypes().values()
                if node_type.isManager() and node_type.childTypeCategory() is None
            ]
        )

    return rop_types


def _get_frame_padding(parameter: hou.Parm) -> int:
    """Try to determine the frame padding based on a parameter.

    Args:
        parameter: A parameter with an output path.

    Returns:
        The determined frame padding. If it cannot be determined, returns 1.
    """
    try:
        # Try to get the unexpanded value from the referenced parameter in the event
        # we're executing a node inside a digital asset that's using an expression.
        path_value = parameter.getReferencedParm().unexpandedString()

    # There might still be some expression magic going on though so in the event that
    # we can't get the unexpanded value we'll just skip.
    except hou.OperationFailed:
        result = None

    else:
        result = re.search("\\.\\$F(\\d+)\\.", path_value)

    frame_padding = 1

    if result is not None:
        frame_padding = int(result.group(1))

    return frame_padding


# Functions


def attach_rop_render_event(scriptargs: dict) -> None:
    """Attach render event callbacks to a ROP node.

    Args:
        scriptargs: The event handler script args dict.
    """
    node = scriptargs["node"]

    if isinstance(node, hou.RopNode):
        node.addRenderEventCallback(handle_rop_render_event)


def attach_rop_render_to_all_nodes(scriptargs: dict) -> None:  # pylint: disable=W0613
    """Attach our generic render event callback handler to any ROP nodes in the scene.

    Args:
        scriptargs: The event handler script args dict.
    """
    instances = _find_all_rop_instances()

    # Add our render callback to all the instances.
    for instance in instances:
        instance.addRenderEventCallback(handle_rop_render_event)


def handle_rop_render_event(
    node: hou.RopNode, render_event: hou.ropRenderEventType, scene_time: float
) -> None:
    """The ROP render event handler.

    Args:
        node: The ROP node being executed.
        render_event: The type of render event.
        scene_time: The scene evaluation time.
    """
    process = RopRenderFactory().get_process_for_node(node)

    event_args = {"scene_time": scene_time}

    if render_event == hou.ropRenderEventType.PreRender:
        process.pre_render(event_args)

    elif render_event == hou.ropRenderEventType.PreFrame:
        process.pre_frame(event_args)

    elif render_event == hou.ropRenderEventType.PostFrame:
        process.post_frame(event_args)

        if not process.has_post_write:
            process.post_write(event_args)

    elif render_event == hou.ropRenderEventType.PostWrite:
        process.post_write(event_args)

    elif render_event == hou.ropRenderEventType.PostRender:
        process.post_render(event_args)


def print_pre_render(event_args: dict) -> None:
    """Print the pre render output.

    Args:
        event_args: The event args.
    """
    print(f"Starting Render {event_args['node'].path()}")


def print_post_frame(event_args: dict) -> None:
    """Print the post frame output.

    Args:
        event_args: The event args.
    """
    frame = hou.timeToFrame(event_args["scene_time"])

    padding = event_args["frame_padding"]

    if hou.almostEqual(frame, round(frame)):
        frame_str = f"{round(frame):0{padding}d}"
    else:
        frame_str = str(int(frame)) if frame.is_integer() else f"{frame:.3f}"

    print(f"Frame {frame_str} complete {event_args['frame_time']:.3f}s")


def print_post_write(event_args: dict) -> None:
    """Print the post file write output.

    Args:
        event_args: The event args.
    """
    if "output_path" in event_args:
        file_path = event_args["output_path"]

        if file_path.startswith("temp:"):
            return

        size = pathlib.Path(file_path).stat().st_size
        print(f"Wrote {file_path} ({humanfriendly.format_size(size)})")


def print_post_render(event_args: dict) -> None:
    """Print the post render output.

    Args:
        event_args: The event args.
    """
    print(
        f"Finished Rendering {event_args['node'].path()}: {event_args['render_count']} total {event_args['render_time']:.3f}s"  # noqa: E501
    )
