====================
Other Houdini Events
====================

Various other events may be emitted. Some of these are detailed below:


externaldragdrop.py
-------------------

Houdini allows for a ``scripts/externaldragdrop.py`` file to exist in the ``HOUDINI_PATH`` which can respond to files
being dropped on a Houdini session. This file will emit the :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniSessionEvent.ExternalDragDrop`
event.

The dropped files are available via ``scriptargs["file_paths"]``.  If your callback can handle the dropped files it
should set ``scriptargs[constants.DRAG_DROP_ACCEPTED] = True`` to indicate to the calling code that it was handled and
thus not defer to Houdini to try and handle it.

Consider the following example where we want to handle dropping some sort of file on Houdini.

.. code-block:: python

    def my_drop_handler(scriptargs):
        can_handle = any([file_path for file_path in scriptargs["file_paths"]
            if Path(file_path).suffix == {some file type extension}
        ])

        # It is not necessary to add `constants.DRAG_DROP_ACCEPTED = False` as it will be implied
        # if not present.
        if not can_handle:
            return

        for file_path in scriptargs["file_paths"]:
            # do something to handle the file

        scriptargs[constants.DRAG_DROP_ACCEPTED] = True


    CallbackManager().addCallback(HoudiniSessionEvent.ExternalDragDrop, my_drop_handler)

Since Houdini itself is responsible for handling the dropping of hip files, an event will not be emitted in the case
the dropped file is `.hip, .hiplc, .hipnc.`


nodegraphhooks.py
-----------------

The ``nodegraphhooks.py`` file located in the ``PYTHONPATH`` (usually under ``pythonX.Ylibs``) can be used to intercept
events in the network editor.

Please see the documentation on `nodegraphhooks.py <https://www.sidefx.com/docs/houdini/hom/network.html#intercepting-events-globally>`_
for more information on handling events.

Event Data
^^^^^^^^^^

The occurring ``canvaseventtypes.KeyboardEvent`` is available via the ``scriptargs["uievent"]`` value.

Marking Events as Handled
^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to the above drag and drop event, network editor event callbacks need to return information as to whether they
handled any event.  For :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniNodeGraphEvent.PostKeyboardEvent` you
should set ``scriptargs[constants.KEYBOARD_EVENT_HANDLED] = True`` to indicate that the callback handled the event.

Emitted Events
^^^^^^^^^^^^^^

HoudiniNodeGraphEvent.PostPasteEvent
''''''''''''''''''''''''''''''''''''

The :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniNodeGraphEvent.PostPasteEvent` will be emitted when items are
pasted.

The pasted items are available via the ``scriptargs[constants.PASTED_ITEMS]`` value.


HoudiniNodeGraphEvent.PostKeyboardEvent
'''''''''''''''''''''''''''''''''''''''

The :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniNodeGraphEvent.PostKeyboardEvent` will be emitted when a known
key is pressed.

The supplied pending actions are available via the ``scriptargs["pending_actions"]`` data.


Houdini Session Close
---------------------

The :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniSessionEvent.HoudiniClose` will be emitted when Houdini is about
to close.

This event is emitted via the standard :py:mod:`atexit` mechanism.
