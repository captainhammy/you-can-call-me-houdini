"""Test the externaldragdrop.py module."""

# Future
from __future__ import annotations

# Standard Library
import os
import sys
from typing import TYPE_CHECKING

# Third Party
import pytest

# You Can Call Me Houdini
from you_can_call_me_houdini import events
from you_can_call_me_houdini.api import constants, manager

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

# Add the directory which contains externaldragdrop.py to the path so we can import it.
if "REZ_YOU_CAN_CALL_ME_HOUDINI_ROOT" in os.environ:
    sys.path.append(os.environ["REZ_YOU_CAN_CALL_ME_HOUDINI_ROOT"] + "/houdini/scripts")

else:
    sys.path.append("src/houdini/scripts")

# You Can Call Me Houdini
import externaldragdrop

# Fixtures


@pytest.fixture
def clean_manager(monkeypatch: pytest.MonkeyPatch) -> manager.CallbackManager:
    """Fixture that provides a CallbackManager object with no callbacks."""
    mgr = manager.CallbackManager()

    monkeypatch.setattr(mgr, "callbacks", {})

    return mgr


# Tests


@pytest.mark.parametrize(
    ("test_paths", "expected"),
    [
        (["/path/to/file.hip"], True),
        (["/path/to/file.hiplc"], True),
        (["/path/to/file.hipnc"], True),
        (["/path/to/file.hiprc"], False),
        (["/path/to/thing.txt", "/path/to/file.hip"], True),
    ],
)
def test__contains_any_hip_files(test_paths: list[str], expected: bool) -> None:
    """Test externaldragdrop._contains_any_hip_files()."""
    result = externaldragdrop._contains_any_hip_files(test_paths)

    assert result == expected


@pytest.mark.parametrize(
    ("has_hips", "accepted", "expected"),
    [
        (True, True, False),
        (False, False, False),
        (False, True, True),
    ],
)
def test_dropAccept(
    mocker: MockerFixture, clean_manager: manager.CallbackManager, has_hips: bool, accepted: bool, expected: bool
) -> None:
    """Test externaldragdrop.dropAccept()."""

    def test_func(scriptargs):  # noqa: ANN001, ANN202
        if accepted:
            scriptargs[constants.DRAG_DROP_ACCEPTED] = True

    clean_manager.add_callback(events.HoudiniSessionEvent.ExternalDragDrop, test_func)

    mocker.patch("externaldragdrop._contains_any_hip_files", return_value=has_hips)

    mock_paths = mocker.MagicMock(spec=list)

    result = externaldragdrop.dropAccept(mock_paths)

    assert result == expected
