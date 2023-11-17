"""Perform tasks when external files are dropped onto the Houdini window."""

# Standard Library
from pathlib import Path
from typing import List

# You Can Call Me Houdini
import you_can_call_me_houdini.events
from you_can_call_me_houdini.api import constants
from you_can_call_me_houdini.api.manager import CallbackManager

# Non-Public Functions


def _contains_any_hip_files(file_paths: List[str]) -> bool:
    """Check if any of the dropped files are hip files.

    This will only match explicit known hip file types:
        - .hip
        - .hiplc
        - .hipnc

    If you were to drop a compressed file of type .hip.gz this would not return True.

    Args:
        file_paths: The list of files to check.

    Returns:
        Whether any of the file paths are hip files.
    """
    hip_extensions = (".hip", ".hiplc", ".hipnc")

    return any(
        file_path
        for file_path in file_paths
        if Path(file_path).suffix in hip_extensions
    )


# Functions


def dropAccept(file_paths: List[str]) -> bool:  # pylint: disable=invalid-name
    """Accept a list of files.

    This function is called by Houdini when files are dropped onto the UI.

    Args:
        file_paths: A list of dropped files.

    Returns:
        Whether the drop was handled.
    """
    # Let Houdini handle dropping .hip files.
    if _contains_any_hip_files(file_paths):
        return False

    scriptargs = {"file_paths": file_paths}

    CallbackManager().emit(
        you_can_call_me_houdini.events.HoudiniSessionEvent.ExternalDragDrop, scriptargs
    )

    # Return whether the drop was accepted by the handler.
    return bool(scriptargs.get(constants.DRAG_DROP_ACCEPTED, False))
