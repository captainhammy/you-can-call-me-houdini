"""Test the OnInstall.py script."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniNodeEvent

# Houdini
import hou

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest_mock import MockerFixture

# Tests


def test_OnInstall(mocker: MockerFixture, execute_houdini_script: Callable[[str, dict], None]) -> None:
    """Test the OnInstall.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("OnInstall", {"node": hou.node("/obj")})

    mock_emit.assert_called_with(HoudiniNodeEvent.OnInstall, {"node": hou.node("/obj")})
