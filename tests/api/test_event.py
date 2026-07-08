"""Tests for the you_can_call_me_houdini.api.event module."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# Third Party
import pytest

# You Can Call Me Houdini
import you_can_call_me_houdini.api.event

# Houdini
import hou

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

# Tests


class TestHoudiniEventEnum:
    """Test the you_can_call_me_houdini.api.event.HoudiniEventEnum object."""

    @pytest.mark.parametrize("function_type", [False, True])
    def test_log_message(self, mocker: MockerFixture, function_type: bool) -> None:
        """Test HoudiniEventEnum.log_message()."""
        mock_logger = mocker.patch("you_can_call_me_houdini.api.event.event_logger")

        class TestEnum(you_can_call_me_houdini.api.event.HoudiniEventEnum):
            Test = 1

        def test_func():  # noqa: ANN202
            pass

        class NoNameCallable:
            def __init__(self):  # noqa: ANN204
                pass

            def __call__(self):  # noqa: ANN204
                pass

        callable_item = test_func if function_type else NoNameCallable

        mock_args = mocker.MagicMock(spec=dict)

        TestEnum.Test.log_message(callable_item, mock_args)

        if function_type:
            assert mock_logger.debug.call_args.args[2] == f"{callable_item.__module__}.{callable_item.__name__}()"

        else:
            assert mock_logger.debug.call_args.args[2] == f"{callable_item.__module__}()"


class TestHoudiniNodeEventEnum:
    """Test the you_can_call_me_houdini.api.event.HoudiniNodeEventEnum object."""

    @pytest.mark.parametrize("function_type", [False, True])
    def test_log_message(self, mocker: MockerFixture, function_type: bool) -> None:
        """Test HoudiniNodeEventEnum.log_message()."""
        mock_logger = mocker.patch("you_can_call_me_houdini.api.event.event_logger")

        class TestEnum(you_can_call_me_houdini.api.event.HoudiniNodeEventEnum):
            Test = 1

        def test_func():  # noqa: ANN202
            pass

        class NoNameCallable:
            def __init__(self):  # noqa: ANN204
                pass

            def __call__(self):  # noqa: ANN204
                pass

        callable_item = test_func if function_type else NoNameCallable

        test_args = {"node": mocker.MagicMock(spec=hou.Node)}

        TestEnum.Test.log_message(callable_item, test_args)

        if function_type:
            assert mock_logger.debug.call_args.args[2] == f"{callable_item.__module__}.{callable_item.__name__}()"

        else:
            assert mock_logger.debug.call_args.args[2] == f"{callable_item.__module__}()"

        assert test_args["node"].path() in mock_logger.debug.call_args.args


class TestEvent:
    """Test the you_can_call_me_houdini.api.event.Event object."""

    @pytest.mark.parametrize("post_report", [False, True])
    def test___pos_init__(self, post_report: bool) -> None:
        """Test Event.__post_init__()."""
        inst = you_can_call_me_houdini.api.event.Event("test", stats_post_report=post_report)
        assert inst.stats.post_report == post_report


class TestRunOnceEvent:
    """Test the you_can_call_me_houdini.api.event.RunOnceEvent object."""

    def test_post_run_callback(self) -> None:
        """Test RunOnceEvent.post_run_callback()."""
        inst = you_can_call_me_houdini.api.event.RunOnceEvent("test")

        assert inst.enabled
        inst.post_run_callback()
        assert not inst.enabled
