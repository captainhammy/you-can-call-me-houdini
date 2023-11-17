=================
Default Callbacks
=================

A number of callbacks are added for execution by default by ``you_can_call_me_houdini``:

Execution of 123.cmd
--------------------

If Houdini is started without a hip file, :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.NoHip`
will execute a callback that sources a found ``scripts/123.cmd`` file.


Addition of ROP Render Callbacks
--------------------------------

In order to ROP render events to be able to emit events using ``you_can_call_me_houdini`` it is necessary to explicitly
add callbacks to ROP nodes in order to emit these.

When :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniNodeEvent.OnCreated` is emitted, if a node is a :py:class:`hou.RopNode`
then it will have a render event callback that runs emitting code registered to it.


When :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniSessionEvent.SceneLoaded` is emitted, all found :py:class:`hou.RopNode`
instances will have a render event callback that runs emitting code registered to them.


ROP Render Progress Output
--------------------------

Making use of the above mentioned addition of ROP Render callbacks, when certain render events are completed information
will be output.

You can disable the default progress callbacks by setting ``$YOU_CAN_CALL_ME_HOUDINI_DISABLE_ROP_EVENTS=1``
