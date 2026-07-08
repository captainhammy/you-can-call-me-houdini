"""Test the beforescenesave.py script."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniSessionEvent

# Houdini
import hou

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest_mock import MockerFixture

# Tests


def test_beforescenesave(mocker: MockerFixture, execute_houdini_script: Callable[[str, dict], None]) -> None:
    """Test the beforescenesave.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("beforescenesave", {"node": hou.node("/obj")})

    mock_emit.assert_called_with(HoudiniSessionEvent.BeforeSceneSave, {"node": hou.node("/obj")})
