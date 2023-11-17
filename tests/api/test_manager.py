"""Tests for the you_can_call_me_houdini.api.manager module."""

# Third Party
import pytest
import pytest_houdini.tools

# You Can Call Me Houdini
from you_can_call_me_houdini.api import event, manager
from you_can_call_me_houdini.events import HoudiniSessionEvent


@pytest.fixture
def test_manager():
    """A CallbackManager for testing.

    The `callbacks` dict is cleared after each test.
    """

    inst = manager.CallbackManager()

    yield inst

    inst.callbacks.clear()


@pytest.fixture
def test_enum():
    class TestEnum(event.HoudiniEventEnum):
        FOO = event.Event("foo")
        BAR = event.Event("bar", enabled=False)
        BAZ = event.Event("baz")

    yield TestEnum


class TestCallbackManager:
    """Test the you_can_call_me_houdini.api.manager.CallbackManager object."""

    def test___init__(self):
        """Test object initialization."""
        inst = manager.CallbackManager()
        assert inst.callbacks == {}

    @pytest.mark.parametrize(
        "ui_available,skip_no_ui,expect_result,test_name",
        (
            (False, True, False, None),
            (False, False, True, None),
            (True, False, True, None),
            (True, False, True, "test_name"),
        ),
    )
    def test_add_callback(
        self,
        mocker,
        test_manager,
        test_enum,
        ui_available,
        skip_no_ui,
        expect_result,
        test_name,
    ):
        """Test CallbackManager.add_callback()."""
        mocker.patch("hou.isUIAvailable", return_value=ui_available)

        def test_func():
            pass

        result = test_manager.add_callback(
            test_enum.FOO,
            test_func,
            name=test_name,
            skip_no_ui=skip_no_ui,
        )

        if expect_result:
            assert result.name == test_name if test_name is not None else "test_func"

        else:
            assert result is None

    @pytest.mark.parametrize(
        "tester,event_enum,enabled,pass_args",
        (
            (pytest.raises(TypeError), None, True, False),
            (
                pytest_houdini.tools.does_not_raise(),
                HoudiniSessionEvent.NewScene,
                False,
                False,
            ),
            (
                pytest_houdini.tools.does_not_raise(),
                HoudiniSessionEvent.NewScene,
                True,
                False,
            ),
            (
                pytest_houdini.tools.does_not_raise(),
                HoudiniSessionEvent.NewScene,
                True,
                True,
            ),
        ),
    )
    def test_emit(
        self, mocker, test_manager, test_enum, tester, event_enum, enabled, pass_args
    ):
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

        with tester:
            test_manager.emit(event_enum, test_args)

        if pass_args:
            assert test_args == {"dummy_arg": 123}

        if event_enum and enabled:
            mock_post.assert_called()

    @pytest.mark.parametrize(
        "enabled,has_callbacks",
        (
            (False, True),
            (True, False),
            (True, True),
        ),
    )
    def test_get_callbacks_for_event(
        self, mocker, test_manager, test_enum, enabled, has_callbacks
    ):
        """Test CallbackManager.get_callbacks_for_event()."""
        test_enum.FOO.value.enabled = enabled

        callbacks = mocker.MagicMock(spec=list) if has_callbacks else []

        test_manager.callbacks[test_enum.FOO] = callbacks

        result = test_manager.get_callbacks_for_event(test_enum.FOO)

        if enabled and has_callbacks:
            assert result == callbacks

        else:
            assert result == []

    def test_ignore_event_callbacks(self, test_manager, test_enum):
        """Test CallbackManager.ignore_event_callbacks()."""
        counter_args = {
            "c1": 0,
            "c2": 0,
            "c3": 0,
        }

        def func1(scriptargs):
            scriptargs["c1"] += 1

        def func2(scriptargs):
            scriptargs["c2"] += 1

        def func3(scriptargs):
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
