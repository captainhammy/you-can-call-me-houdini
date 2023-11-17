"""Package logging related functions."""

# Standard Library
import importlib.resources
import json
import logging.config

# Functions


def init_config() -> None:
    """Load logger config from file."""
    config_file = importlib.resources.files("you_can_call_me_houdini.api").joinpath(
        "logging_config.json"
    )

    with config_file.open(encoding="UTF-8") as handle:
        config = json.load(handle)
        logging.config.dictConfig(config)
