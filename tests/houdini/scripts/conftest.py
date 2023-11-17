"""Fixtures for testing houdini/scripts code."""

# Standard Library
import pathlib

# Third Party
import pytest

# Fixtures


@pytest.fixture
def execute_houdini_script():
    """Execute a script under houdini/scripts."""

    def _exec(script_name, kwargs):
        script_path = pathlib.Path(f"src/houdini/scripts/{script_name}.py")

        if not script_path.exists():
            script_path = pathlib.Path(f"src/houdini/scripts/_{script_name}.py")

        with script_path.open() as handle:
            contents = handle.read()

        exec(contents, {"kwargs": kwargs})

    yield _exec
