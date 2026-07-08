"""Fixtures for testing houdini/scripts code."""

# Future
from __future__ import annotations

# Standard Library
import pathlib
from typing import TYPE_CHECKING

# Third Party
import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

# Fixtures


@pytest.fixture
def execute_houdini_script() -> Callable[[str, dict], None]:
    """Execute a script under houdini/scripts."""

    def _exec(script_name: str, kwargs: dict) -> None:
        script_path = pathlib.Path(f"src/houdini/scripts/{script_name}.py")

        if not script_path.exists():
            script_path = pathlib.Path(f"src/houdini/scripts/_{script_name}.py")

        contents = script_path.read_text()

        exec(contents, {"kwargs": kwargs})  # noqa: S102

    return _exec
