"""Tests for the you_can_call_me_houdini.api.callback module."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini.api import callback, constants
from you_can_call_me_houdini.events import HoudiniSessionEvent

if TYPE_CHECKING:
    from collections.abc import Callable
    from unittest.mock import MagicMock

    from pytest_mock import MockerFixture

# Fixtures


@pytest.fixture
def dummy_callback(mocker: MockerFixture) -> MagicMock:
    """Fixture to return a mocked test function."""
    return mocker.MagicMock(spec=callable)


@pytest.fixture
def init_test_callback(mocker: MockerFixture) -> Callable:
    """Initialize an empty Callback option for testing."""
    mocker.patch.object(callback.Callback, "__init__", lambda x, y, z, w: None)

    def _create_test_class() -> callback.Callback:
        return callback.Callback(None, None, None)  # type: ignore

    return _create_test_class


# Tests


class TestCallback:
    """Test the you_can_call_me_houdini.api.callback.Callback object."""

    def test___init__(self, dummy_callback: Callable) -> None:
        """Test object initialization."""
        result = callback.Callback("test_init", dummy_callback)

        assert result.callback_function == dummy_callback
        assert result.enabled
        assert result.name == "test_init"

    @pytest.mark.parametrize("enabled", [True, False])
    def test___call__(self, mocker: MockerFixture, dummy_callback: MagicMock, enabled: bool) -> None:
        """Test Callback.__call__()."""
        expected_calls = []

        inst = callback.Callback("test_call", dummy_callback, enabled=enabled)

        test_args = {constants.CALLBACK_EVENT_TYPE: HoudiniSessionEvent.HoudiniClose}

        if enabled:
            expected_calls.append(mocker.call(test_args))

        inst(test_args)

        dummy_callback.assert_has_calls(expected_calls)
