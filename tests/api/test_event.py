"""Tests for the you_can_call_me_houdini.api.event module."""

# Third Party
import pytest

# You Can Call Me Houdini
import you_can_call_me_houdini.api.event

# Tests


class TestHoudiniEventEnum:
    """Test the you_can_call_me_houdini.api.event.HoudiniEventEnum object."""

    def test_log_message(self, mocker):
        """Test HoudiniEventEnum.log_message()."""
        mock_logger = mocker.patch("you_can_call_me_houdini.api.event.event_logger")

        class TestEnum(you_can_call_me_houdini.api.event.HoudiniEventEnum):
            Test = 1

        mock_func = mocker.MagicMock(spec=callable)
        mock_args = mocker.MagicMock(spec=dict)

        TestEnum.Test.log_message(mock_func, mock_args)

        mock_logger.debug.assert_called()


class TestEvent:
    """Test the you_can_call_me_houdini.api.event.Event object."""

    @pytest.mark.parametrize("post_report", (False, True))
    def test___pos_init__(self, post_report):
        """Test Event.__post_init__()."""
        inst = you_can_call_me_houdini.api.event.Event(
            "test", stats_post_report=post_report
        )
        assert inst.stats.post_report == post_report


class TestRunOnceEvent:
    """Test the you_can_call_me_houdini.api.event.RunOnceEvent object."""

    def test_post_run_callback(self):
        inst = you_can_call_me_houdini.api.event.RunOnceEvent("test")

        assert inst.enabled
        inst.post_run_callback()
        assert not inst.enabled
