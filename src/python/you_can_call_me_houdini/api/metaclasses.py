"""This module contains metaclasses for use in you_can_call_me_houdini."""

# Future
from __future__ import annotations


class Singleton(type):
    """Singleton implementation as a metaclass."""

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):  # type: ignore
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
