"""Tests for the you_can_call_me_houdini.events module."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# You Can Call Me Houdini
import you_can_call_me_houdini.events

# Houdini
import hou

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

# Tests


class TestHoudiniNodeEvent:
    """Test the you_can_call_me_houdini.events.HoudiniNodeEvent object."""

    def test_log_message(self, mocker: MockerFixture) -> None:
        """Test HoudiniNodeEvent.log_message()."""
        mock_logger = mocker.patch("you_can_call_me_houdini.api.event.event_logger")

        def test_func(scriptargs):  # noqa: ANN001, ANN202
            pass

        mock_node = mocker.MagicMock(spec=hou.OpNode)
        test_args = {
            "node": mock_node,
        }

        you_can_call_me_houdini.events.HoudiniNodeEvent.OnCreated.log_message(test_func, test_args)

        mock_logger.debug.assert_called_with(
            "%s: %s '%s'",
            you_can_call_me_houdini.events.HoudiniNodeEvent.OnCreated,
            "tests.test_events.test_func()",
            mock_node.path.return_value,
        )


class TestRopRenderEvent:
    """Test the you_can_call_me_houdini.events.RopRenderEvent object."""

    def test_log_message(self, mocker: MockerFixture) -> None:
        """Test RopRenderEvent.log_message()."""
        mock_logger = mocker.patch("you_can_call_me_houdini.api.event.event_logger")

        def test_func(scriptargs):  # noqa: ANN001, ANN202
            pass

        mock_node = mocker.MagicMock(spec=hou.OpNode)
        test_args = {
            "node": mock_node,
        }

        you_can_call_me_houdini.events.RopRenderEvent.PreRender.log_message(test_func, test_args)

        mock_logger.debug.assert_called_with(
            "%s: %s '%s'",
            you_can_call_me_houdini.events.RopRenderEvent.PreRender,
            "tests.test_events.test_func()",
            mock_node.path.return_value,
        )
