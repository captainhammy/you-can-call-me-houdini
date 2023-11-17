"""This module contains classes related to event statistics."""

# Future
from __future__ import annotations

# Standard Library
import time
from dataclasses import dataclass, field
from types import TracebackType

# Classes


@dataclass
class EventStats:
    """This class is used to track event stats

    Args:
        name: The event name to associate the stats with.
        post_report: Whether to print the stats report after execution.
    """

    name: str
    post_report: bool = False
    run_count: int = field(default=0, init=False)
    last_run_time: float = field(default=0, repr=False, init=False)
    last_started: float = field(default=0, repr=False, init=False)
    total_time: float = field(default=0, init=False)

    def __enter__(self) -> None:
        self.last_started = time.time()

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        end = time.time()

        self.last_run_time = end - self.last_started
        self.total_time += self.last_run_time

        self.run_count += 1

        if self.post_report:
            self.print_report()

    # Methods

    def print_report(self) -> None:
        """Print (log) a stats report for the last run."""
        print(f"Event name: {self.name}")
        print(f"\tRun Count: {self.run_count}")
        print(f"\tRun Time: {self.last_run_time}")

    def reset(self) -> None:
        """Reset all counts."""
        self.last_run_time = 0
        self.run_count = 0
        self.total_time = 0
