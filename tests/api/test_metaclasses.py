"""Tests for the you_can_call_me_houdini.api.metaclasses module."""


# You Can Call Me Houdini
from you_can_call_me_houdini.api import metaclasses


def test_Singleton():
    """Test the you_can_call_me_houdini.api.metaclasses.Singleton object."""

    class TestClass(metaclass=metaclasses.Singleton):
        """Test class for Singleton."""

    inst1 = TestClass()

    inst2 = TestClass()

    assert inst1 is inst2
