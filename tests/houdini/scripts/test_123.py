"""Test the 123.py script."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniStartupEvent

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest_mock import MockerFixture

# Tests


def test_123(mocker: MockerFixture, execute_houdini_script: Callable[[str, dict], None]) -> None:
    """Test the 123.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    execute_houdini_script("123", {})

    mock_emit.assert_called_with(HoudiniStartupEvent.NoHip)
