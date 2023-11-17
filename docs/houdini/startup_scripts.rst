=====================
Startup Script Events
=====================

Please see the documentation on `Houdini Startup Scripts <https://www.sidefx.com/docs/houdini/hom/locations.html#startup>`_
for a description of when each script is executed.

pythonrc.py
-----------

``pythonrc.py`` is used to set up the various base callbacks on Houdini startup and does not emit any events.

123.py / houdinicore.py
-----------------------

The ``123.py`` and ``houdinicore.py`` scripts will emit the :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.NoHip` event.

Each of these scripts will also emit their own specific callbacks (:py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.NoHipCore`,
:py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.NoHipFX`) **before** the
:py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.NoHip` event.


456.py
------

The ``456.py`` script will emit several callbacks when run:

    - :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.HoudiniStarted` (run only the first time 456.py is run)
    - When 456 is run with a hip file
        - :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.SceneLoaded`
    - When 456 is run without a hip file
        - :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.NewScene`
    - :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.Any` (run every time 456.py is run)


ready.py
--------

The ``ready.py`` script will emit the :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniStartupEvent.Ready` event.


uiready.py
----------

The ``uiready.py`` script will emit the :py:enum:mem:`~you_can_call_me_houdini.events.HoudiniUIEvent.UIReady` event.

