"""Tests for the you_can_call_me_houdini.api.logger module."""

# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING

# You Can Call Me Houdini
from you_can_call_me_houdini.api import logger

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

# Tests


def test_init_config(mocker: MockerFixture) -> None:
    """Test you_can_call_me_houdini.api.logger.init_config()."""
    mock_dict_config = mocker.patch("logging.config.dictConfig")

    logger.init_config()

    mock_dict_config.assert_called()
