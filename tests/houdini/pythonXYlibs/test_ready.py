"""Test the ready.py script."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniStartupEvent

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

pytestmark = pytest.mark.usefixtures("add_scripts_python")


# Tests


def test_ready(mocker: MockerFixture) -> None:
    """Test the ready.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    import ready  # noqa: F401

    mock_emit.assert_called_with(HoudiniStartupEvent.Ready)
