# Houdini
import hou

# Backwards compatibility with Houdini 19.x.
if not hasattr(hou, "OpNode"):
    hou.OpNode = hou.Node
