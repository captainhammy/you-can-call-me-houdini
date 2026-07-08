"""Test the uiready.py script."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini.api.manager import CallbackManager
from you_can_call_me_houdini.events import HoudiniUIEvent

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from pytest_mock import MockerFixture

pytestmark = pytest.mark.usefixtures("add_scripts_python")


# Tests


def test_uiready(mocker: MockerFixture, mock_hdefereval: MagicMock) -> None:
    """Test the uiready.py script."""
    mock_emit = mocker.patch.object(CallbackManager, "emit")

    import uiready  # noqa: F401

    mock_emit.assert_called_with(HoudiniUIEvent.UIReady)
