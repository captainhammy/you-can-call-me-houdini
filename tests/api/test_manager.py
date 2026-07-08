"""Tests for the you_can_call_me_houdini.api.manager module."""

# Future
from __future__ import annotations

# Standard Library
from contextlib import nullcontext
from typing import TYPE_CHECKING, Any

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini.api import event, exceptions, manager
from you_can_call_me_houdini.events import HoudiniSessionEvent

if TYPE_CHECKING:
    from collections.abc import Generator

    from pytest_mock import MockerFixture


class EnumTester(event.HoudiniEventEnum):  # noqa: D101
    FOO = event.Event("foo")
    BAR = event.Event("bar", enabled=False)
    BAZ = event.Event("baz")


@pytest.fixture
def test_manager() -> Generator[manager.CallbackManager, Any, None]:
    """A CallbackManager for testing.

    The `callbacks` dict is cleared after each test.
    """
    inst = manager.CallbackManager()

    yield inst

    inst.callbacks.clear()


@pytest.fixture
def test_enum() -> type[EnumTester]:
    """Fixture to provide test event enum class."""
    return EnumTester


class TestCallbackManager:
    """Test the you_can_call_me_houdini.api.manager.CallbackManager object."""

    def test___init__(self) -> None:
        """Test object initialization."""
        # Force clear out any singleton instances that may have already been created.
        manager.CallbackManager._instances.clear()

        inst = manager.CallbackManager()
        assert inst.callbacks == {}

        # Check singleton-ness
        assert inst is manager.CallbackManager()

    @pytest.mark.parametrize(
        ("ui_available", "skip_no_ui", "test_name", "callback_is_function_type", "expected_result_name"),
        [
            (False, True, None, False, "<unknown>"),
            (False, False, None, False, "<unknown>"),
            (True, False, None, False, "<unknown>"),
            (True, False, "test_name", False, "test_name"),
            (True, False, None, True, "test_func"),
        ],
    )
    def test_add_callback(
        self,
        mocker: MockerFixture,
        test_manager: manager.CallbackManager,
        test_enum: type[EnumTester],
        ui_available: bool,
        skip_no_ui: bool,
        test_name: str | None,
        callback_is_function_type: bool,
        expected_result_name: str,
    ) -> None:
        """Test CallbackManager.add_callback()."""
        expect_result = not (skip_no_ui and not ui_available)

        mocker.patch("hou.isUIAvailable", return_value=ui_available)

        def test_func():  # noqa: ANN202
            pass

        class NoNameCallable:
            def __init__(self):  # noqa: ANN204
                pass

            def __call__(self):  # noqa: ANN204
                pass

        result = test_manager.add_callback(
            test_enum.FOO,
            test_func if callback_is_function_type else NoNameCallable,
            name=test_name,
            skip_no_ui=skip_no_ui,
        )

        if result is None:
            assert expect_result is False

        else:
            assert result.name == expected_result_name

    @pytest.mark.parametrize(
        ("context", "event_enum", "enabled", "pass_args"),
        [
            (pytest.raises(exceptions.InvalidEventTypeError), None, True, False),
            (
                nullcontext(),
                HoudiniSessionEvent.NewScene,
                False,
                False,
            ),
            (
                nullcontext(),
                HoudiniSessionEvent.NewScene,
                True,
                False,
            ),
            (
                nullcontext(),
                HoudiniSessionEvent.NewScene,
                True,
                True,
            ),
        ],
    )
    def test_emit(
        self,
        mocker: MockerFixture,
        test_manager: manager.CallbackManager,
        test_enum: type[EnumTester],
        context: nullcontext | pytest.RaisesExc[exceptions.InvalidEventTypeError],
        event_enum: HoudiniSessionEvent,
        enabled: bool,
        pass_args: bool,
    ) -> None:
        """Test CallbackManager.emit()."""
        mock_func = mocker.MagicMock()
        mock_func.__name__ = "name"

        if event_enum:
            event_enum.value.enabled = enabled
            test_manager.add_callback(event_enum, mock_func)

            mock_post = mocker.patch.object(event_enum.value, "post_run_callback")

        test_args = None

        if pass_args:
            test_args = {"dummy_arg": 123}

        with context:
            test_manager.emit(event_enum, test_args)

        if pass_args:
            assert test_args == {"dummy_arg": 123}

        if event_enum and enabled:
            mock_post.assert_called()

    @pytest.mark.parametrize(
        ("enabled", "has_callbacks"),
        [
            (False, True),
            (True, False),
            (True, True),
        ],
    )
    def test_get_callbacks_for_event(
        self,
        mocker: MockerFixture,
        test_manager: manager.CallbackManager,
        test_enum: type[EnumTester],
        enabled: bool,
        has_callbacks: bool,
    ) -> None:
        """Test CallbackManager.get_callbacks_for_event()."""
        test_enum.FOO.value.enabled = enabled

        callbacks = mocker.MagicMock(spec=list) if has_callbacks else []

        test_manager.callbacks[test_enum.FOO] = callbacks

        result = test_manager.get_callbacks_for_event(test_enum.FOO)

        if enabled and has_callbacks:
            assert result == callbacks

        else:
            assert result == []

    def test_ignore_event_callbacks(self, test_manager: manager.CallbackManager, test_enum: type[EnumTester]) -> None:
        """Test CallbackManager.ignore_event_callbacks()."""
        counter_args = {
            "c1": 0,
            "c2": 0,
            "c3": 0,
        }

        def func1(scriptargs):  # noqa: ANN001, ANN202
            scriptargs["c1"] += 1

        def func2(scriptargs):  # noqa: ANN001, ANN202
            scriptargs["c2"] += 1

        def func3(scriptargs):  # noqa: ANN001, ANN202
            scriptargs["c3"] += 1

        test_manager.add_callback(test_enum.FOO, func1)
        test_manager.add_callback(test_enum.BAR, func2)
        test_manager.add_callback(test_enum.BAZ, func3)

        with test_manager.ignore_event_callbacks():
            test_manager.emit(test_enum.FOO, counter_args)
            test_manager.emit(test_enum.BAR, counter_args)
            test_manager.emit(test_enum.BAZ, counter_args)

        assert counter_args["c1"] == 0
        assert counter_args["c2"] == 0
        assert counter_args["c3"] == 0

        with test_manager.ignore_event_callbacks(test_enum.BAZ):
            test_manager.emit(test_enum.FOO, counter_args)
            test_manager.emit(test_enum.BAZ, counter_args)

        assert counter_args["c1"] == 1
        assert counter_args["c3"] == 0

        with test_manager.ignore_event_callbacks([test_enum.BAZ]):
            test_manager.emit(test_enum.FOO, counter_args)
            test_manager.emit(test_enum.BAZ, counter_args)

        assert counter_args["c1"] == 2
        assert counter_args["c3"] == 0
