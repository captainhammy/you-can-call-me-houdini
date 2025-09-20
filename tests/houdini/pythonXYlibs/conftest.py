"""Fixtures for testing houdini/pythonX.Ylibs code."""

# Standard Library
import os
import pathlib
import sys

# Third Party
import pytest

# Fixtures


@pytest.fixture
def add_pythonxylibs(monkeypatch):
    """Add the appropriate pythonX.Ylibs folder to the start of sys.path."""
    if "HOUDINI_PACKAGE_TESTING" in os.environ:
        libs_dir = (
            pathlib.Path(os.environ["REZ_YOU_CAN_CALL_ME_HOUDINI_ROOT"])
            / "houdini"
            / f"python{sys.version_info.major}.{sys.version_info.minor}libs"
        )

    else:
        libs_dir = pathlib.Path.cwd() / "src/houdini/pythonX.Ylibs"

    monkeypatch.syspath_prepend(libs_dir)


@pytest.fixture
def add_scripts_python(monkeypatch):
    """Add the houdini/scripts/python to the start of sys.path."""
    if "HOUDINI_PACKAGE_TESTING" in os.environ:
        python_dir = pathlib.Path(os.environ["REZ_YOU_CAN_CALL_ME_HOUDINI_ROOT"]) / "houdini" / "scripts" / "python"

    else:
        python_dir = pathlib.Path.cwd() / "src/houdini/scripts/python"

    monkeypatch.syspath_prepend(python_dir)
