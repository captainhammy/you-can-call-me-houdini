========
Examples
========


Registering a simple callback
-----------------------------

The following code example adds a super simple callback when a node is created.

.. code-block:: python

    from you_can_call_me_houdini.api.manager import CallbackManager
    from you_can_call_me_houdini.events import HoudiniNodeEvent

    def on_create_example(scriptargs: dict) -> None:
        """Simple function to print the created node's path."""
        print(f"I just created {scriptargs['node'].path()}!")

    CallbackManager().add_callback(HoudiniNodeEvent.OnCreated, on_create_example)
