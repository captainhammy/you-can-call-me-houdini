"""Fixtures for testing houdini/pythonX.Ylibs code."""

# Standard Library
import pathlib
import sys

# Third Party
import pytest

# Fixtures


@pytest.fixture
def add_pythonxylibs(monkeypatch):
    """Add the appropriate pythonX.Ylibs folder to the start of sys.path."""
    libs_dir = (
        pathlib.Path.cwd()
        / f"src/houdini/python{sys.version_info.major}.{sys.version_info.minor}libs"
    )
    monkeypatch.syspath_prepend(libs_dir)
