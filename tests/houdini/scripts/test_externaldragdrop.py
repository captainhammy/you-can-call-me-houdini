"""Test the externaldragdrop.py module."""

# Standard Library
import sys

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini import events
from you_can_call_me_houdini.api import constants, manager

# Add the directory which contains externaldragdrop.py to the path so we can import it.
sys.path.append("src/houdini/scripts")

# You Can Call Me Houdini
import externaldragdrop

# Fixtures


@pytest.fixture
def clean_manager(monkeypatch):
    """Fixture that provides a CallbackManager object with no callbacks."""
    mgr = manager.CallbackManager()

    monkeypatch.setattr(mgr, "callbacks", {})

    yield mgr


# Tests


@pytest.mark.parametrize(
    "test_paths, expected",
    (
        (["/path/to/file.hip"], True),
        (["/path/to/file.hiplc"], True),
        (["/path/to/file.hipnc"], True),
        (["/path/to/file.hiprc"], False),
        (["/path/to/thing.txt", "/path/to/file.hip"], True),
    ),
)
def test__contains_any_hip_files(test_paths, expected):
    """Test externaldragdrop._contains_any_hip_files()."""
    result = externaldragdrop._contains_any_hip_files(test_paths)

    assert result == expected


@pytest.mark.parametrize(
    "has_hips, accepted, expected",
    (
        (True, True, False),
        (False, False, False),
        (False, True, True),
    ),
)
def test_dropAccept(mocker, clean_manager, has_hips, accepted, expected):
    """Test externaldragdrop.dropAccept()."""

    def test_func(scriptargs):
        if accepted:
            scriptargs[constants.DRAG_DROP_ACCEPTED] = True

    clean_manager.add_callback(events.HoudiniSessionEvent.ExternalDragDrop, test_func)

    mocker.patch("externaldragdrop._contains_any_hip_files", return_value=has_hips)

    mock_paths = mocker.MagicMock(spec=list)

    result = externaldragdrop.dropAccept(mock_paths)

    assert result == expected
