"""Tests for the you_can_call_me_houdini.api.logger module."""

# You Can Call Me Houdini
from you_can_call_me_houdini.api import logger

# Tests


def test_init_config(mocker):
    """Test you_can_call_me_houdini.api.logger.init_config()"""
    mock_dict_config = mocker.patch("logging.config.dictConfig")

    logger.init_config()

    mock_dict_config.assert_called()
