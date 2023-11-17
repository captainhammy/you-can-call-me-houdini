"""Tests for the you_can_call_me_houdini.api.stats module."""

# Standard Library
import time

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini.api import stats

# Tests


class TestEventStats:
    """Test the you_can_call_me_houdini.api.stats.EventStats object."""

    def test___enter__(self):
        """Test EventStats.__enter__()."""
        inst = stats.EventStats("test")

        assert inst.last_started == 0

        inst.__enter__()

        assert inst.last_started > 0

    @pytest.mark.parametrize("print_report", (False, True))
    def test___exit__(self, mocker, print_report):
        """Test EventStats.__exit__()."""
        mock_print = mocker.patch.object(stats.EventStats, "print_report")

        inst = stats.EventStats("test")
        inst.post_report = print_report

        assert inst.last_run_time == 0
        assert inst.total_time == 0
        assert inst.run_count == 0

        with inst:
            time.sleep(0.25)

        assert inst.last_run_time > 0.25
        assert inst.total_time > 0.25
        assert inst.run_count == 1

        assert mock_print.call_count == int(print_report)

        with inst:
            time.sleep(0.5)

        assert inst.last_run_time > 0.5
        assert inst.total_time > 0.75
        assert inst.run_count == 2

    def test_print_report(self, mocker):
        """Test EventStats.print_report()."""
        inst = stats.EventStats("test")

        mock_print = mocker.patch("builtins.print")

        inst.print_report()
        assert mock_print.call_count == 3

    def test_reset(self, mocker):
        """Test EventStats.reset()."""
        inst = stats.EventStats("test")

        inst.last_run_time = 3
        inst.run_count = 2
        inst.total_time = 6

        inst.reset()

        assert inst.last_run_time == 0
        assert inst.run_count == 0
        assert inst.total_time == 0
